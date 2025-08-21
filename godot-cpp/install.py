from dope_common import *
from git import Repo
import argparse
import sys
import shutil
import os

def make_platform():
	if sys.platform == "win32":
		return "windows"
	elif sys.platform == "linux":
		return "linux"
	elif sys.platform == "darwin":
		return "osx"
	else:
		raise ValueError(f"Unsupported platform: {sys.platform}")

def run_scons(src_dir, platform, options, verbose):
	cmd  = f'scons'
	cmd += f' -C {src_dir}'
	cmd += f' platform={platform}'
	cmd += f' {options}'
	cmd += f' -j 4'
	run(cmd, verbose)

def get_library_suffix():
	if sys.platform == "win32":
		return "lib"
	elif sys.platform == "linux":
		return "a"
	elif sys.platform == "darwin":
		return "a"

def copy_headers(src_dir, install_dir):
	# recursively find header files in src_dir and install them to install_dir,
	# maintaining the folder structure
	for root, dirs, files in os.walk(src_dir):
		for file in files:
			if file.endswith(".h") or file.endswith(".hpp"):
				# Get the relative path from src_dir to maintain folder structure
				rel_path = os.path.relpath(root, src_dir)
				# Create destination directory path
				dest_dir = os.path.join(install_dir, rel_path)
				# Create destination file path
				dest_file = os.path.join(dest_dir, file)
				
				# Ensure destination directory exists
				os.makedirs(dest_dir, exist_ok=True)
				
				shutil.copy(os.path.join(root, file), dest_file)

def cmake_configure(src_dir, build_dir, install_dir, verbose):
	cmake_cmd = 'cmake'
	cmake_cmd += f' -B "{build_dir}"'
	cmake_cmd += f' -S "{src_dir}"'
	cmake_cmd += f' -DCMAKE_PREFIX_PATH="{install_dir}"'
	cmake_cmd += f' -DCMAKE_INSTALL_PREFIX="{install_dir}"'
	run(cmake_cmd, verbose)

def cmake_install(build_dir, verbose):
	run(f'cmake --install {build_dir}', verbose)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--root", type=str, required=True)
	parser.add_argument("--assets", type=str, required=True)
	parser.add_argument("--clean", action="store_true")
	parser.add_argument("--verbose", action="store_true")
	args = parser.parse_args()
	dep = {}
	dep["name"] = "godot-cpp"
	src_dir     = make_dep_src_dir(dep, args.root)
	repo = Repo(src_dir)
	repo.git.submodule('update', '--init', '--recursive')
	platform = make_platform()
	install_dir = make_install_dir(args.root)
	install_lib_dir = os.path.join(install_dir, "lib")
	lib_suffix = get_library_suffix()
	build_lib_debug = os.path.join(src_dir, "bin", f'libgodot-cpp.{platform}.debug.64.{lib_suffix}')
	build_lib_release = os.path.join(src_dir, "bin", f'libgodot-cpp.{platform}.release.64.{lib_suffix}')
	if not os.path.exists(build_lib_debug):
		run_scons(src_dir, platform, "target=debug generate_bindings=yes", args.verbose)
	if not os.path.exists(build_lib_release):
		run_scons(src_dir, platform, "target=release", args.verbose)
	build_dir = make_dep_build_dir(dep, "none", args.root)
	cmake_configure(src_dir, build_dir, install_dir, args.verbose)
	cmake_install(build_dir, args.verbose)