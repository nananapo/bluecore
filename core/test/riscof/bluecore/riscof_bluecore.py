import os
import re
import shutil
import subprocess
import shlex
import logging
import random
import string
from string import Template
import sys

import riscof.utils as utils
import riscof.constants as constants
from riscof.pluginTemplate import pluginTemplate

from elftools.elf.elffile import ELFFile
def get_section_address(filepath, section_name):
  try:
      with open(filepath, 'rb') as f:
          elffile = ELFFile(f)
          for section in elffile.iter_sections():
              if section.name == section_name:
                  return section.header['sh_addr']
          return 0
  except:
      return 0

logger = logging.getLogger()

class bluecore(pluginTemplate):
    __model__ = "bluecore"

    #TODO: please update the below to indicate family, version, etc of your DUT.
    __version__ = "XXX"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config = kwargs.get('config')

        # If the config node for this DUT is missing or empty. Raise an error. At minimum we need
        # the paths to the ispec and pspec files
        if config is None:
            print("Please enter input file paths in configuration.")
            raise SystemExit(1)

        # In case of an RTL based DUT, this would be point to the final binary executable of your
        # test-bench produced by a simulator (like verilator, vcs, incisive, etc). In case of an iss or
        # emulator, this variable could point to where the iss binary is located. If 'PATH variable
        # is missing in the config.ini we can hardcode the alternate here.
        self.dut_exe = config['PATH']

        # Number of parallel jobs that can be spawned off by RISCOF
        # for various actions performed in later functions, specifically to run the tests in
        # parallel on the DUT executable. Can also be used in the build function if required.
        self.num_jobs = str(config['jobs'] if 'jobs' in config else 1)

        # Path to the directory where this python file is located. Collect it from the config.ini
        self.pluginpath=os.path.abspath(config['pluginpath'])

        # Collect the paths to the  riscv-config absed ISA and platform yaml files. One can choose
        # to hardcode these here itself instead of picking it from the config.ini file.
        self.isa_spec = os.path.abspath(config['ispec'])
        self.platform_spec = os.path.abspath(config['pspec'])

        #We capture if the user would like the run the tests on the target or
        #not. If you are interested in just compiling the tests and not running
        #them on the target, then following variable should be set to False
        if 'target_run' in config and config['target_run']=='0':
            self.target_run = False
        else:
            self.target_run = True
        
        self.bin2hex_path = os.path.abspath(config["BIN2HEX_PATH"])
        self.bootrom_path = os.path.abspath(config["BOOTROM_PATH"])

    def initialise(self, suite, work_dir, archtest_env):

       # capture the working directory. Any artifacts that the DUT creates should be placed in this
       # directory. Other artifacts from the framework and the Reference plugin will also be placed
       # here itself.
       self.work_dir = work_dir

       # capture the architectural test-suite directory.
       self.suite_dir = suite

       # Note the march is not hardwired here, because it will change for each
       # test. Similarly the output elf name and compile macros will be assigned later in the
       # runTests function
       self.compile_cmd = 'riscv{1}-unknown-elf-gcc -march={0} \
         -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles -g -mno-relax\
         -T '+self.pluginpath+'/env/link.ld\
         -I '+self.pluginpath+'/env/\
         -I ' + archtest_env + ' {2} -o {3} {4}'

       # add more utility snippets here

    def build(self, isa_yaml, platform_yaml):

      # load the isa yaml as a dictionary in python.
      ispec = utils.load_yaml(isa_yaml)['hart0']

      # capture the XLEN value by picking the max value in 'supported_xlen' field of isa yaml. This
      # will be useful in setting integer value in the compiler string (if not already hardcoded);
      self.xlen = ('64' if 64 in ispec['supported_xlen'] else '32')

      # for bluecore start building the '--isa' argument. the self.isa is dutnmae specific and may not be
      # useful for all DUTs
      self.isa = 'rv' + self.xlen
      if "I" in ispec["ISA"]:
          self.isa += 'i'
      if "M" in ispec["ISA"]:
          self.isa += 'm'
      if "F" in ispec["ISA"]:
          self.isa += 'f'
      if "D" in ispec["ISA"]:
          self.isa += 'd'
      if "C" in ispec["ISA"]:
          self.isa += 'c'

      #TODO: The following assumes you are using the riscv-gcc toolchain. If
      #      not please change appropriately
      self.compile_cmd = self.compile_cmd+' -mabi='+('lp64 ' if 64 in ispec['supported_xlen'] else 'ilp32 ')

    def runTests(self, testList):

      # we will iterate over each entry in the testList. Each entry node will be referred to by the
      # variable testname.
      for testname in testList:

          logger.debug('Running Test: {0} on DUT'.format(testname))
          # for each testname we get all its fields (as described by the testList format)
          testentry = testList[testname]

          # we capture the path to the assembly file of this test
          test = testentry['test_path']

          # capture the directory where the artifacts of this test will be dumped/created.
          test_dir = testentry['work_dir']

          # name of the elf file after compilation of the test
          elf = 'my.elf'

          # name of the signature file as per requirement of RISCOF. RISCOF expects the signature to
          # be named as DUT-<dut-name>.signature. The below variable creates an absolute path of
          # signature file.
          sig_file = os.path.join(test_dir, self.name[:-1] + ".signature")

          # for each test there are specific compile macros that need to be enabled. The macros in
          # the testList node only contain the macros/values. For the gcc toolchain we need to
          # prefix with "-D". The following does precisely that.
          compile_macros= ' -D' + " -D".join(testentry['macros'])

          # collect the march string required for the compiler
          marchstr = testentry['isa'].lower()

          # substitute all variables in the compile command that we created in the initialize
          # function
          cmd = self.compile_cmd.format(marchstr, self.xlen, test, elf, compile_macros)

          # just a simple logger statement that shows up on the terminal
          logger.debug('Compiling test: ' + test)

          # the following command spawns a process to run the compile command. Note here, we are
          # changing the directory for this command to that pointed by test_dir. If you would like
          # the artifacts to be dumped else where change the test_dir variable to the path of your
          # choice.
          utils.shellCommand(cmd).run(cwd=test_dir)

          # for debug purposes if you would like stop the DUT plugin after compilation, you can
          # comment out the lines below and raise a SystemExit

          logfile = str(elf) + ".log"
          bin2hex_granularity = 4 if self.xlen == '32' else 8

          if self.target_run:
            # dump
            cmd = "riscv{0}-unknown-elf-objdump -S {1} > {2}.dump".format(self.xlen, elf, elf)
            utils.shellCommand(cmd).run(cwd=test_dir)
            # elf -> bin
            cmd = "riscv{0}-unknown-elf-objcopy -O binary {1} {2}.bin".format(self.xlen, elf, elf)
            utils.shellCommand(cmd).run(cwd=test_dir)
            # bin -> hex
            cmd = "python3 {0} {1} {2}.bin > {3}.hex".format(self.bin2hex_path, bin2hex_granularity, elf, elf)
            utils.shellCommand(cmd).run(cwd=test_dir)
            # run test
            execute = "DBG_ADDR={0} ".format(get_section_address(os.path.join(test_dir, elf), ".tohost"))
            execute += "{0} {1} {2}.hex 1000000 > {3}".format(self.dut_exe, self.bootrom_path, str(elf), logfile)
            logger.debug('Executing on bluecore ' + execute)


          # launch the execute command. Change the test_dir if required.
          utils.shellCommand(execute).run(cwd=test_dir)

          # save the signature
          signatures = []
          signature_granularity = 8
          with open(test_dir + "/" + logfile, mode="r") as fd:
            lines = fd.readlines()
            prefix = "signature: "
            for l in lines:
                if not l.startswith(prefix):
                    continue
                signatures.append(l[len(prefix):len(prefix) + signature_granularity])
          with open(sig_file, mode="w") as fd:
            signatures = list(map(lambda s: s + "\n", signatures))
            fd.writelines(signatures)

      # if target runs are not required then we simply exit as this point after running all
      # the makefile targets.
      if not self.target_run:
          raise SystemExit