import sublime, sublime_plugin, subprocess, thread, os, functools, glob, fnmatch

class JumpToTestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		current_file = self.view.file_name()
		self.base_dir = current_file.partition("/src/")[0]
		if current_file.endswith("Test.scala"):
			target_file = current_file.replace("/test/", "/main/").replace("Test.scala", ".scala")
		else:
			target_file = current_file.replace("/main/", "/test/").replace(".scala", "Test.scala")
		if not os.path.exists(target_file):
			sublime.error_message("could not find " + target_file)
		self.view.window().open_file(target_file)

class BaseScalaTestCommand(sublime_plugin.TextCommand):
	def load_config(self):
		s = sublime.load_settings("ScalaTest.sublime-settings")
		global SCALA; SCALA = s.get("scala_exec")
		global useScalaTest; useScalaTest = s.get("use_scala_test") == "true"

	def run(self, edit):
		self.load_config()
		self.show_tests_panel()
		self.base_dir = self.view.file_name().partition("/src/")[0]
		runner = "org.scalatest.tools.Runner -s " if useScalaTest else "org.junit.runner.JUnitCore "
		scala_args = "-cp target/classes:target/test-classes:`find lib/default/*.jar | tr '\012' ':'`:`find lib/test/*.jar | tr '\012' ':'` "+ runner + \
			self.junit_args()
		command = wrap_in_cd(self.base_dir, SCALA + " " + scala_args)
		self.proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		thread.start_new_thread(self.read_stdout, ())
		thread.start_new_thread(self.read_stderr, ())

	def relative_path_to_class_name(self, partition_folder, relative_path, suffix):
		return relative_path.rpartition(partition_folder + "/")[2].replace("/", ".").replace(suffix, "")

	def read_stdout(self):
		self.copy_stream_to_output_view(self.proc.stdout)

	def read_stderr(self):
		self.copy_stream_to_output_view(self.proc.stderr)

	def copy_stream_to_output_view(self, stream):
		while True:
			data = os.read(stream.fileno(), 2**15)

			if data != "":
				sublime.set_timeout(functools.partial(self.append_data, self.proc, data), 0)
			else:
				stream.close()
				break		

	def window(self):
		return self.view.window()

	def append_data(self, proc, data):
		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.insert(edit, self.output_view.size(), data)
		self.output_view.end_edit(edit)
		self.output_view.set_read_only(True)

	def show_tests_panel(self):
		if not hasattr(self, 'output_view'):
			self.output_view = self.window().get_output_panel("tests")
		self.clear_test_view()
		self.window().run_command("show_panel", {"panel": "output.tests"})

	def clear_test_view(self):
		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
		self.output_view.end_edit(edit)
		self.output_view.set_read_only(True)

class ScalaTestCommand(BaseScalaTestCommand):
	def junit_args(self):
		return self.relative_path_to_class_name("scala", self.view.file_name(), ".scala")

class ScalaTestAllCommand(BaseScalaTestCommand):
	def junit_args(self):
		matches = []
		for root, dirnames, filenames in os.walk(self.base_dir + '/target'):
			for filename in fnmatch.filter(filenames, '*Test.class'):
				matches.append(self.relative_path_to_class_name("classes", os.path.join(root, filename), ".class"))
		test_classes = " ".join(matches)

		return test_classes

class JumpToScalaFile(sublime_plugin.TextCommand):
	def run(self, edit):
		self.base_dir = self.view.file_name().partition("/src/")[0]
		self.files = []
		for root, dirnames, filenames in os.walk(self.base_dir):
			for filename in fnmatch.filter(filenames, '*.scala'):
				self.files.append(os.path.join(root, filename))
		file_names = map(lambda x: os.path.split(x)[1], self.files)
		sublime.active_window().show_quick_panel(file_names, self.file_selected)

	def file_selected(self, selected_index):
		if selected_index != -1:
			sublime.active_window().open_file(self.files[selected_index])

def wrap_in_cd(path, command):
	return 'cd ' + path.replace("\\", "/") + ' && ' + command
