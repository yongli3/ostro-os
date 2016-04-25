"""
@file test_gyro_lsm330dlc.py
"""
##
# @addtogroup soletta sensor
# @brief This is sensor test based on soletta app
# @brief test sensor lsm330dlc on Galileo/MinnowMax/Edison
##
import os
import time
from oeqa.utils.helper import shell_cmd
from oeqa.oetest import oeRuntimeTest
from EnvirSetup import EnvirSetup
from oeqa.utils.decorators import tag

@tag(TestType="FVT", FeatureID="IOTOS-757")
class TestGyroLSM330DLC(oeRuntimeTest):
    """
    @class TestGyroLSM330DLC
    """
    def setUp(self):
        '''Generate fbp file on target
        @fn setUp
        @param self
        @return'''
        print 'start!\n'
        #connect sensor and DUT through board
        #shell_cmd("sudo python "+ os.path.dirname(__file__) + "/Connector.py lsm330dlc")
        envir = EnvirSetup(self.target)
        envir.envirSetup("lsm330dlc","gyro")

    def tearDown(self):
        '''unload lsm330dlc driver
        @fn tearDown
        @param self
        @return'''
        (status, output) = self.target.run("cat /sys/devices/virtual/dmi/id/board_name")
        if "Minnow" in output:
           (status, output) = self.target.run(
                         "cd /sys/bus/i2c/devices; \
                          echo 0x6b >i2c-1/delete_device")
        if "Galileo" in output:
           (status, output) = self.target.run(
                         "cd /sys/bus/i2c/devices; \
                          echo 0x6b >i2c-0/delete_device")
        if "BODEGA" in output:
           (status, output) = self.target.run(
                         "cd /sys/bus/i2c/devices; \
                          echo 0x6b >i2c-6/delete_device")
        
    def test_Gyro_LSM330DLC(self):
        '''Execute the test app and verify sensor data
        @fn test_Gyro_LSM330DLC
        @param self
        @return'''
        print 'start reading data!'
        (status, output) = self.target.run(
                         "chmod 777 /opt/apps/test_gyro_lsm330dlc.fbp")
        (status, output) = self.target.run(
                         "cd /opt/apps; ./test_gyro_lsm330dlc.fbp >re.log")        
        error = output
        (status, output) = self.target.run(
                         "cp /opt/apps/re.log /home/root/lsm330dlc.log")         
        (status, output) = self.target.run("cat /opt/apps/re.log|grep direction-vector")
        print output + "\n"
        self.assertEqual(status, 0, msg="Error messages: %s" % error) 
        #make sure sensor data is valid 
        (status, output) = self.target.run("cat /opt/apps/re.log|grep '0.000000, 0.000000, 0.000000'")
        self.assertEqual(status, 1, msg="Error messages: %s" % output)      
