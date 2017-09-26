"""
Created on Apr 12, 2017

@author: sgoldsmith

Copyright (c) Steven P. Goldsmith

All rights reserved.
"""

import ConfigParser, cv2


class config(object):
    """Configuration class.
    
    This make it easy to pass around app configuration.

    """
    
    # Event type attributes
    motionStart, motionStop, pedestrianDetected, cascadeDetected, circleDetected, startRecording, stopRecording, healthCheck = range(0, 8)    

    def __init__(self, fileName):
        """ Read configuration from INI file """
        parser = ConfigParser.SafeConfigParser()
        # Read configuration file
        parser.read(fileName)
        """Configure from INI file"""
        # Logging related attributes
        self.loggingLevel = parser.get("logging", "level")
        self.loggingFormatter = parser.get("logging", "formatter") 
        # Set camera related data attributes
        self.cameraName = parser.get("camera", "name")
        self.framePlugin = parser.get("camera", "framePlugin")
        self.videoCaptureProperties = eval(parser.get("camera", "videoCaptureProperties"))
        self.videoloopPlugins = eval(parser.get("camera", "videoloopPlugins"), {}, {})
        self.url = parser.get("camera", "url")
        self.socketTimeout = parser.getint("camera", "socketTimeout")
        self.resizeWidthDiv = parser.getint("camera", "resizeWidthDiv")
        self.detectPlugin = parser.get("camera", "detectPlugin")
        self.fpsInterval = parser.getfloat("camera", "fpsInterval")
        self.fps = parser.getint("camera", "fps")
        self.frameBufMax = parser.getint("camera", "frameBufMax")
        self.fourcc = parser.get("camera", "fourcc")
        self.recordFileExt = parser.get("camera", "recordFileExt")
        self.recordDir = parser.get("camera", "recordDir")
        self.mark = parser.getboolean("camera", "mark")
        self.saveFrames = parser.getboolean("camera", "saveFrames")
        # Set motion related data attributes
        self.ignoreMask = parser.get("motion", "ignoreMask")
        self.kSize = eval(parser.get("motion", "kSize"), {}, {})
        self.alpha = parser.getfloat("motion", "alpha")
        self.blackThreshold = parser.getint("motion", "blackThreshold")
        self.maxChange = parser.getfloat("motion", "maxChange")
        self.startThreshold = parser.getfloat("motion", "startThreshold")
        self.stopThreshold = parser.getfloat("motion", "stopThreshold")
        self.historyImage = parser.getboolean("motion", "historyImage")
        # Set contour related data attributes
        self.dilateAmount = parser.getint("motion", "dilateAmount")
        self.erodeAmount = parser.getint("motion", "erodeAmount")
        # Set pedestrian detect related data attributes
        self.hitThreshold = parser.getfloat("pedestrian", "hitThreshold")
        self.winStride = eval(parser.get("pedestrian", "winStride"), {}, {})
        self.padding = eval(parser.get("pedestrian", "padding"), {}, {})
        self.scale0 = parser.getfloat("pedestrian", "scale0")
        self.minHogWeight = parser.getfloat("pedestrian", "minHogWeight")
        # Set cascade related data attributes
        self.cascadeFile = parser.get("cascade", "cascadeFile")
        self.scaleFactor = parser.getfloat("cascade", "scaleFactor")
        self.minNeighbors = parser.getint("cascade", "minNeighbors")
        self.minWidth = parser.getint("cascade", "minWidth")
        self.minHeight = parser.getint("cascade", "minHeight")
        self.minCascadeWeight = parser.getint("cascade", "minCascadeWeight")
        # Set Hough Circles related attributes
        self.methodType = int(eval(parser.get("hough", "methodType")))
        self.dp = parser.getint("hough", "dp")
        self.minDist = parser.getint("hough", "minDist")
        self.param1 = parser.getint("hough", "param1")
        self.param2 = parser.getint("hough", "param2")
        self.minRadius = parser.getint("hough", "minRadius")
        self.maxRadius = parser.getint("hough", "maxRadius")
        # Set SCP related attributes
        self.hostName = parser.get("scp", "hostName")
        self.userName = parser.get("scp", "userName")
        self.remoteDir = parser.get("scp", "remoteDir")
        self.timeout = parser.getint("scp", "timeout")
        self.deleteSource = parser.getboolean("scp", "deleteSource")        
        # Set health check related attributes
        self.healthFileName = parser.get("health", "healthFileName")
        self.healthMqttHost = parser.get("health", "healthMqttHost")
        self.healthMqttPort = parser.getint("health", "healthMqttPort")
        self.healthMqttTopic = parser.get("health", "healthMqttTopic")
