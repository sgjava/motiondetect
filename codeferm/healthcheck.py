"""
Created on Apr 23, 2017

@author: sgoldsmith

Copyright (c) Steven P. Goldsmith

All rights reserved.
"""

import os, threading, observer


class healthcheck(observer.observer):
    """Health check.
    
    Verify the health of videoloop. External process needs to monitor file mtime
    since file will not be updated if health check fails. Make sure the external
    process is aware of the file update interval set in fpsInterval.
    
    """
    
    def __init__(self, appConfig, logger):
        self.appConfig = appConfig
        self.logger = logger
        self.mqttc = None
        if self.appConfig.healthMqttHost:
            try:
                self.logger.info("Enabling Health MQTT to %s:%d" % (self.appConfig.healthMqttHost, self.appConfig.healthMqttPort))
                import paho.mqtt.client as mqtt

                self.mqttc = mqtt.Client()

                self.mqttc.connect(self.appConfig.healthMqttHost, self.appConfig.healthMqttPort, 60)
                mqttThread = threading.Thread(target=self.mqttLoop)
                mqttThread.daemon = True
                mqttThread.start()

            except Exception, e:
                self.logger.exception("Could not connect to MQTT Broker. MQTT Disabled")
                self.mqttEnabled = False
                
    def check(self, frameBuf, fps, frameOk):
        """Verify videoloop health"""
        message = ""

        if len(frameBuf) <= fps * 2 and frameOk:
            message = "OK"        
        else:
            message = "NOT OK"
        
        self.logger.info("Health " + message)

        if self.appConfig.healthFileName:
            fileName = os.path.expanduser(self.appConfig.healthFileName)
            fileDir = os.path.dirname(fileName)
            # Create dir if it doesn"t exist
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            # Write to health check file      
            with open(fileName, 'a') as f:
                f.write(message + " ")

        if self.mqttc is not None:
            self.mqttc.publish(self.appConfig.healthMqttTopic, message)

    def mqttLoop(self):
        self.mqttc.loop_forever()

    def observeEvent(self, **kwargs):
        "Handle events"
        if kwargs["event"] == self.appConfig.healthCheck:
            # Kick off health check thread


            healthThread = threading.Thread(target=self.check, args=(kwargs["frameBuf"], kwargs["fps"], kwargs["frameOk"],))
            healthThread.start()
