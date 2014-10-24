import json
import os

import sublime
import sublime_plugin

messages = {
	"dialog": {
		"session_name": "Enter session name:"
	},
	"error": {
		"default": "Unknown error!"
	}
}

def error_msg(error_code):
	error_code = str(error_code)
	key = error_code if error_code in messages["error"] else "default"

	return messages["error"][key] + " (%s)".format(error_code)


class SaveSession(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel(messages["dialog"]["session_name"], self.generate_name(), self.save_session)

	def generate_name(self):
		pass

	def save_session(self, session_name):
		pass
