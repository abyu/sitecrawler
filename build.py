from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.integrationtest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

default_task = "publish"

@init
def initialize(project):
  project.set_property("verbose", True)

  project.build_depends_on('mock')
  project.build_depends_on('mockito')
  project.depends_on("requests")