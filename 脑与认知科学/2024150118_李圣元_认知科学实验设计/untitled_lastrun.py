#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.2.3),
    on 九月 15, 2026, at 10:52
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.2.3'
expName = 'untitled'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = (1024, 768)
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = 'data/' + expInfo['participant'] + '_' + expName + '_' + expInfo['date']
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='D:\\课件\\脑与认知科学\\实验一\\untitled_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    # store pilot mode in data file
    thisExp.addData('piloting', PILOTING, priority=priority.LOW)
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=True,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "welcome" ---
    text = visual.TextStim(win=win, name='text',
        text='！！！欢迎来到实验！！！\n\n本次实验有两个部分：\n1）点击你最感兴趣的图片\n2）点击你最喜欢的颜色\n点击左键可以开始',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    mouse_to_open = event.Mouse(win=win)
    x, y = [None, None]
    mouse_to_open.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "text_test1" ---
    prompt = visual.TextStim(win=win, name='prompt',
        text='！！！实验一！！！\n\n在本次实验中，会左右陈列两张照片\n请您根据自己喜好用鼠标选择其中一张照片。\n准备好了可以点击鼠标左键开始',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    mouse_to_test1 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_to_test1.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "trial1" ---
    cat = visual.ImageStim(
        win=win,
        name='cat', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.25, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    dog = visual.ImageStim(
        win=win,
        name='dog', 
        image='default.png', mask=None, anchor='center-right',
        ori=0.0, pos=(0.5, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "feedback_test1" ---
    feedback_to_test1 = visual.TextStim(win=win, name='feedback_to_test1',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "text_test2" ---
    text_2 = visual.TextStim(win=win, name='text_2',
        text='！！！实验二！！！\n\n在这次实验中会显示两个不同的三角形\n请您根据提示词的颜色选择其中一张颜色符合的\n使用按键左右进行操作',
        font='SimHei',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "trial2" ---
    left_one = visual.ShapeStim(
        win=win, name='left_one',
        size=(0.25, 0.25), vertices='triangle',
        ori=0.0, pos=(-0.25, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    right_one = visual.ShapeStim(
        win=win, name='right_one',
        size=(0.25, 0.25), vertices='triangle',
        ori=0.0, pos=(0.25, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    textbox_to_prompt = visual.TextBox2(
         win, text='', placeholder='Type here...', font='SimHei',
         ori=0.0, pos=(0, 0), draggable=False,      letterHeight=0.05,
         size=(0.5, 0.5), borderWidth=2.0,
         color='white', colorSpace='rgb',
         opacity=None,
         bold=False, italic=False,
         lineSpacing=1.0, speechPoint=None,
         padding=0.0, alignment='center',
         anchor='center', overflow='visible',
         fillColor=None, borderColor=None,
         flipHoriz=False, flipVert=False, 
         languageStyle='LTR',
         formattingSyntax='md',
         editable=False,
         name='textbox_to_prompt',
         depth=-2, autoLog=True,
    )
    key_resp = keyboard.Keyboard(deviceName='defaultKeyboard', backend='PsychToolbox')
    
    # --- Initialize components for Routine "feedback_tesst2" ---
    feedback_test2 = visual.TextStim(win=win, name='feedback_test2',
        text='',
        font='SimHei',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "endtest" ---
    endtest_text = visual.TextStim(win=win, name='endtest_text',
        text='实验结束\n感谢您的参与',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "welcome" ---
    # create an object to store info about Routine welcome
    welcome = data.Routine(
        name='welcome',
        components=[text, mouse_to_open],
    )
    welcome.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse_to_open
    mouse_to_open.x = []
    mouse_to_open.y = []
    mouse_to_open.leftButton = []
    mouse_to_open.midButton = []
    mouse_to_open.rightButton = []
    mouse_to_open.time = []
    gotValidClick = False  # until a click is received
    # store start times for welcome
    welcome.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    welcome.tStart = globalClock.getTime(format='float')
    welcome.status = STARTED
    thisExp.addData('welcome.started', welcome.tStart)
    welcome.maxDuration = None
    # keep track of which components have finished
    welcomeComponents = welcome.components
    for thisComponent in welcome.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "welcome" ---
    thisExp.currentRoutine = welcome
    welcome.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # if text is stopping this frame...
        if text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                text.tStop = t  # not accounting for scr refresh
                text.tStopRefresh = tThisFlipGlobal  # on global time
                text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.stopped')
                # update status
                text.status = FINISHED
                text.setAutoDraw(False)
        # *mouse_to_open* updates
        
        # if mouse_to_open is starting this frame...
        if mouse_to_open.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_to_open.frameNStart = frameN  # exact frame index
            mouse_to_open.tStart = t  # local t and not account for scr refresh
            mouse_to_open.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_to_open, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_to_open.started', t)
            # update status
            mouse_to_open.status = STARTED
            mouse_to_open.mouseClock.reset()
            # if button is down already this ISN'T a new click
            mouse_to_open.prevButtonState = mouse_to_open.getPressed()
        
        # if mouse_to_open is stopping this frame...
        if mouse_to_open.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > mouse_to_open.tStartRefresh + 3-frameTolerance:
                # keep track of stop time/frame for later
                mouse_to_open.tStop = t  # not accounting for scr refresh
                mouse_to_open.tStopRefresh = tThisFlipGlobal  # on global time
                mouse_to_open.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData('mouse_to_open.stopped', t)
                # update status
                mouse_to_open.status = FINISHED
        if mouse_to_open.status == STARTED:  # only update if started and not finished!
            buttons = mouse_to_open.getPressed()
            # button state changed?
            if buttons != mouse_to_open.prevButtonState:
                mouse_to_open.prevButtonState = buttons
                # state changed to a new click
                if sum(buttons) > 0:
                    pass
                    x, y = mouse_to_open.getPos()
                    mouse_to_open.x.append(float(x))
                    mouse_to_open.y.append(float(y))
                    buttons = mouse_to_open.getPressed()
                    mouse_to_open.leftButton.append(buttons[0])
                    mouse_to_open.midButton.append(buttons[1])
                    mouse_to_open.rightButton.append(buttons[2])
                    mouse_to_open.time.append(mouse_to_open.mouseClock.getTime())
                    
                    continueRoutine = False  # end routine on response
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=welcome,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            welcome.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if welcome.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in welcome.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "welcome" ---
    for thisComponent in welcome.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for welcome
    welcome.tStop = globalClock.getTime(format='float')
    welcome.tStopRefresh = tThisFlipGlobal
    thisExp.addData('welcome.stopped', welcome.tStop)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('mouse_to_open.x', mouse_to_open.x)
    thisExp.addData('mouse_to_open.y', mouse_to_open.y)
    thisExp.addData('mouse_to_open.leftButton', mouse_to_open.leftButton)
    thisExp.addData('mouse_to_open.midButton', mouse_to_open.midButton)
    thisExp.addData('mouse_to_open.rightButton', mouse_to_open.rightButton)
    thisExp.addData('mouse_to_open.time', mouse_to_open.time)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if welcome.maxDurationReached:
        routineTimer.addTime(-welcome.maxDuration)
    elif welcome.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "text_test1" ---
    # create an object to store info about Routine text_test1
    text_test1 = data.Routine(
        name='text_test1',
        components=[prompt, mouse_to_test1],
    )
    text_test1.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse_to_test1
    mouse_to_test1.x = []
    mouse_to_test1.y = []
    mouse_to_test1.leftButton = []
    mouse_to_test1.midButton = []
    mouse_to_test1.rightButton = []
    mouse_to_test1.time = []
    gotValidClick = False  # until a click is received
    # store start times for text_test1
    text_test1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    text_test1.tStart = globalClock.getTime(format='float')
    text_test1.status = STARTED
    thisExp.addData('text_test1.started', text_test1.tStart)
    text_test1.maxDuration = None
    # keep track of which components have finished
    text_test1Components = text_test1.components
    for thisComponent in text_test1.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "text_test1" ---
    thisExp.currentRoutine = text_test1
    text_test1.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *prompt* updates
        
        # if prompt is starting this frame...
        if prompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            prompt.frameNStart = frameN  # exact frame index
            prompt.tStart = t  # local t and not account for scr refresh
            prompt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(prompt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'prompt.started')
            # update status
            prompt.status = STARTED
            prompt.setAutoDraw(True)
        
        # if prompt is active this frame...
        if prompt.status == STARTED:
            # update params
            pass
        
        # if prompt is stopping this frame...
        if prompt.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > prompt.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                prompt.tStop = t  # not accounting for scr refresh
                prompt.tStopRefresh = tThisFlipGlobal  # on global time
                prompt.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'prompt.stopped')
                # update status
                prompt.status = FINISHED
                prompt.setAutoDraw(False)
        # *mouse_to_test1* updates
        
        # if mouse_to_test1 is starting this frame...
        if mouse_to_test1.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_to_test1.frameNStart = frameN  # exact frame index
            mouse_to_test1.tStart = t  # local t and not account for scr refresh
            mouse_to_test1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_to_test1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_to_test1.started', t)
            # update status
            mouse_to_test1.status = STARTED
            mouse_to_test1.mouseClock.reset()
            # if button is down already this ISN'T a new click
            mouse_to_test1.prevButtonState = mouse_to_test1.getPressed()
        
        # if mouse_to_test1 is stopping this frame...
        if mouse_to_test1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > mouse_to_test1.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                mouse_to_test1.tStop = t  # not accounting for scr refresh
                mouse_to_test1.tStopRefresh = tThisFlipGlobal  # on global time
                mouse_to_test1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData('mouse_to_test1.stopped', t)
                # update status
                mouse_to_test1.status = FINISHED
        if mouse_to_test1.status == STARTED:  # only update if started and not finished!
            buttons = mouse_to_test1.getPressed()
            # button state changed?
            if buttons != mouse_to_test1.prevButtonState:
                mouse_to_test1.prevButtonState = buttons
                # state changed to a new click
                if sum(buttons) > 0:
                    pass
                    x, y = mouse_to_test1.getPos()
                    mouse_to_test1.x.append(float(x))
                    mouse_to_test1.y.append(float(y))
                    buttons = mouse_to_test1.getPressed()
                    mouse_to_test1.leftButton.append(buttons[0])
                    mouse_to_test1.midButton.append(buttons[1])
                    mouse_to_test1.rightButton.append(buttons[2])
                    mouse_to_test1.time.append(mouse_to_test1.mouseClock.getTime())
                    
                    continueRoutine = False  # end routine on response
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=text_test1,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            text_test1.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if text_test1.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in text_test1.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "text_test1" ---
    for thisComponent in text_test1.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for text_test1
    text_test1.tStop = globalClock.getTime(format='float')
    text_test1.tStopRefresh = tThisFlipGlobal
    thisExp.addData('text_test1.stopped', text_test1.tStop)
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('mouse_to_test1.x', mouse_to_test1.x)
    thisExp.addData('mouse_to_test1.y', mouse_to_test1.y)
    thisExp.addData('mouse_to_test1.leftButton', mouse_to_test1.leftButton)
    thisExp.addData('mouse_to_test1.midButton', mouse_to_test1.midButton)
    thisExp.addData('mouse_to_test1.rightButton', mouse_to_test1.rightButton)
    thisExp.addData('mouse_to_test1.time', mouse_to_test1.time)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if text_test1.maxDurationReached:
        routineTimer.addTime(-text_test1.maxDuration)
    elif text_test1.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    loop1 = data.TrialHandler2(
        name='loop1',
        nReps=3, 
        method='fullRandom', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('image/chose_dog_or_cat.xlsx'), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(loop1)  # add the loop to the experiment
    thisLoop1 = loop1.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLoop1.rgb)
    if thisLoop1 != None:
        for paramName in thisLoop1:
            globals()[paramName] = thisLoop1[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisLoop1 in loop1:
        loop1.status = STARTED
        if hasattr(thisLoop1, 'status'):
            thisLoop1.status = STARTED
        currentLoop = loop1
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisLoop1.rgb)
        if thisLoop1 != None:
            for paramName in thisLoop1:
                globals()[paramName] = thisLoop1[paramName]
        
        # --- Prepare to start Routine "trial1" ---
        # create an object to store info about Routine trial1
        trial1 = data.Routine(
            name='trial1',
            components=[cat, dog, mouse],
        )
        trial1.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        cat.setImage(cat_path)
        dog.setImage(dog_path)
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.corr = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        # store start times for trial1
        trial1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial1.tStart = globalClock.getTime(format='float')
        trial1.status = STARTED
        thisExp.addData('trial1.started', trial1.tStart)
        trial1.maxDuration = None
        # keep track of which components have finished
        trial1Components = trial1.components
        for thisComponent in trial1.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial1" ---
        thisExp.currentRoutine = trial1
        trial1.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 2.0:
            # if trial has changed, end Routine now
            if hasattr(thisLoop1, 'status') and thisLoop1.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *cat* updates
            
            # if cat is starting this frame...
            if cat.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                cat.frameNStart = frameN  # exact frame index
                cat.tStart = t  # local t and not account for scr refresh
                cat.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cat, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cat.started')
                # update status
                cat.status = STARTED
                cat.setAutoDraw(True)
            
            # if cat is active this frame...
            if cat.status == STARTED:
                # update params
                pass
            
            # if cat is stopping this frame...
            if cat.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cat.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    cat.tStop = t  # not accounting for scr refresh
                    cat.tStopRefresh = tThisFlipGlobal  # on global time
                    cat.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'cat.stopped')
                    # update status
                    cat.status = FINISHED
                    cat.setAutoDraw(False)
            
            # *dog* updates
            
            # if dog is starting this frame...
            if dog.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                dog.frameNStart = frameN  # exact frame index
                dog.tStart = t  # local t and not account for scr refresh
                dog.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(dog, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'dog.started')
                # update status
                dog.status = STARTED
                dog.setAutoDraw(True)
            
            # if dog is active this frame...
            if dog.status == STARTED:
                # update params
                pass
            
            # if dog is stopping this frame...
            if dog.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > dog.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    dog.tStop = t  # not accounting for scr refresh
                    dog.tStopRefresh = tThisFlipGlobal  # on global time
                    dog.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'dog.stopped')
                    # update status
                    dog.status = FINISHED
                    dog.setAutoDraw(False)
            # *mouse* updates
            
            # if mouse is starting this frame...
            if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mouse.frameNStart = frameN  # exact frame index
                mouse.tStart = t  # local t and not account for scr refresh
                mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('mouse.started', t)
                # update status
                mouse.status = STARTED
                mouse.mouseClock.reset()
                # if button is down already this ISN'T a new click
                mouse.prevButtonState = mouse.getPressed()
            
            # if mouse is stopping this frame...
            if mouse.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > mouse.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    mouse.tStop = t  # not accounting for scr refresh
                    mouse.tStopRefresh = tThisFlipGlobal  # on global time
                    mouse.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData('mouse.stopped', t)
                    # update status
                    mouse.status = FINISHED
            if mouse.status == STARTED:  # only update if started and not finished!
                buttons = mouse.getPressed()
                # button state changed?
                if buttons != mouse.prevButtonState:
                    mouse.prevButtonState = buttons
                    # state changed to a new click
                    if sum(buttons) > 0:
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        clickableList = environmenttools.getFromNames([cat,dog], namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(mouse):
                                gotValidClick = True
                                mouse.clicked_name.append(obj.name)
                        if not gotValidClick:
                            mouse.clicked_name.append(None)
                        # check whether click was in correct object
                        if gotValidClick:
                            _corr = 0
                            _corrAns = environmenttools.getFromNames([], namespace=locals())
                            for obj in _corrAns:
                                # is this object clicked on?
                                if obj.contains(mouse):
                                    _corr = 1
                            mouse.corr.append(_corr)
                        x, y = mouse.getPos()
                        mouse.x.append(float(x))
                        mouse.y.append(float(y))
                        buttons = mouse.getPressed()
                        mouse.leftButton.append(buttons[0])
                        mouse.midButton.append(buttons[1])
                        mouse.rightButton.append(buttons[2])
                        mouse.time.append(mouse.mouseClock.getTime())
                        
                        continueRoutine = False  # end routine on response
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=trial1,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                trial1.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if trial1.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in trial1.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial1" ---
        for thisComponent in trial1.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial1
        trial1.tStop = globalClock.getTime(format='float')
        trial1.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial1.stopped', trial1.tStop)
        # store data for loop1 (TrialHandler)
        loop1.addData('mouse.x', mouse.x)
        loop1.addData('mouse.y', mouse.y)
        loop1.addData('mouse.leftButton', mouse.leftButton)
        loop1.addData('mouse.midButton', mouse.midButton)
        loop1.addData('mouse.rightButton', mouse.rightButton)
        loop1.addData('mouse.time', mouse.time)
        loop1.addData('mouse.corr', mouse.corr)
        loop1.addData('mouse.clicked_name', mouse.clicked_name)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if trial1.maxDurationReached:
            routineTimer.addTime(-trial1.maxDuration)
        elif trial1.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-2.000000)
        
        # --- Prepare to start Routine "feedback_test1" ---
        # create an object to store info about Routine feedback_test1
        feedback_test1 = data.Routine(
            name='feedback_test1',
            components=[feedback_to_test1],
        )
        feedback_test1.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code
        if mouse.clicked_name==["cat"]:
            feedback="cat"
        else:
            feedback="dog"
        feedback_to_test1.setText(feedback)
        # store start times for feedback_test1
        feedback_test1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        feedback_test1.tStart = globalClock.getTime(format='float')
        feedback_test1.status = STARTED
        thisExp.addData('feedback_test1.started', feedback_test1.tStart)
        feedback_test1.maxDuration = None
        # keep track of which components have finished
        feedback_test1Components = feedback_test1.components
        for thisComponent in feedback_test1.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "feedback_test1" ---
        thisExp.currentRoutine = feedback_test1
        feedback_test1.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisLoop1, 'status') and thisLoop1.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *feedback_to_test1* updates
            
            # if feedback_to_test1 is starting this frame...
            if feedback_to_test1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                feedback_to_test1.frameNStart = frameN  # exact frame index
                feedback_to_test1.tStart = t  # local t and not account for scr refresh
                feedback_to_test1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(feedback_to_test1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'feedback_to_test1.started')
                # update status
                feedback_to_test1.status = STARTED
                feedback_to_test1.setAutoDraw(True)
            
            # if feedback_to_test1 is active this frame...
            if feedback_to_test1.status == STARTED:
                # update params
                pass
            
            # if feedback_to_test1 is stopping this frame...
            if feedback_to_test1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > feedback_to_test1.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    feedback_to_test1.tStop = t  # not accounting for scr refresh
                    feedback_to_test1.tStopRefresh = tThisFlipGlobal  # on global time
                    feedback_to_test1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'feedback_to_test1.stopped')
                    # update status
                    feedback_to_test1.status = FINISHED
                    feedback_to_test1.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=feedback_test1,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                feedback_test1.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if feedback_test1.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in feedback_test1.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "feedback_test1" ---
        for thisComponent in feedback_test1.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for feedback_test1
        feedback_test1.tStop = globalClock.getTime(format='float')
        feedback_test1.tStopRefresh = tThisFlipGlobal
        thisExp.addData('feedback_test1.stopped', feedback_test1.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if feedback_test1.maxDurationReached:
            routineTimer.addTime(-feedback_test1.maxDuration)
        elif feedback_test1.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        # mark thisLoop1 as finished
        if hasattr(thisLoop1, 'status'):
            thisLoop1.status = FINISHED
        # if awaiting a pause, pause now
        if loop1.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            loop1.status = STARTED
        thisExp.nextEntry()
        
    # completed 3 repeats of 'loop1'
    loop1.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "text_test2" ---
    # create an object to store info about Routine text_test2
    text_test2 = data.Routine(
        name='text_test2',
        components=[text_2],
    )
    text_test2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for text_test2
    text_test2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    text_test2.tStart = globalClock.getTime(format='float')
    text_test2.status = STARTED
    thisExp.addData('text_test2.started', text_test2.tStart)
    text_test2.maxDuration = None
    # keep track of which components have finished
    text_test2Components = text_test2.components
    for thisComponent in text_test2.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "text_test2" ---
    thisExp.currentRoutine = text_test2
    text_test2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_2* updates
        
        # if text_2 is starting this frame...
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_2.started')
            # update status
            text_2.status = STARTED
            text_2.setAutoDraw(True)
        
        # if text_2 is active this frame...
        if text_2.status == STARTED:
            # update params
            pass
        
        # if text_2 is stopping this frame...
        if text_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > text_2.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                text_2.tStop = t  # not accounting for scr refresh
                text_2.tStopRefresh = tThisFlipGlobal  # on global time
                text_2.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text_2.stopped')
                # update status
                text_2.status = FINISHED
                text_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=text_test2,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            text_test2.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if text_test2.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in text_test2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "text_test2" ---
    for thisComponent in text_test2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for text_test2
    text_test2.tStop = globalClock.getTime(format='float')
    text_test2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('text_test2.stopped', text_test2.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if text_test2.maxDurationReached:
        routineTimer.addTime(-text_test2.maxDuration)
    elif text_test2.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    loop2 = data.TrialHandler2(
        name='loop2',
        nReps=3, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('image/chose_color.xlsx'), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(loop2)  # add the loop to the experiment
    thisLoop2 = loop2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisLoop2.rgb)
    if thisLoop2 != None:
        for paramName in thisLoop2:
            globals()[paramName] = thisLoop2[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisLoop2 in loop2:
        loop2.status = STARTED
        if hasattr(thisLoop2, 'status'):
            thisLoop2.status = STARTED
        currentLoop = loop2
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisLoop2.rgb)
        if thisLoop2 != None:
            for paramName in thisLoop2:
                globals()[paramName] = thisLoop2[paramName]
        
        # --- Prepare to start Routine "trial2" ---
        # create an object to store info about Routine trial2
        trial2 = data.Routine(
            name='trial2',
            components=[left_one, right_one, textbox_to_prompt, key_resp],
        )
        trial2.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        left_one.setFillColor(left_color)
        right_one.setFillColor(right_color)
        textbox_to_prompt.reset()
        textbox_to_prompt.setColor(prompt_color, colorSpace='rgb')
        textbox_to_prompt.setText(prompt_word)
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for trial2
        trial2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial2.tStart = globalClock.getTime(format='float')
        trial2.status = STARTED
        thisExp.addData('trial2.started', trial2.tStart)
        trial2.maxDuration = None
        # keep track of which components have finished
        trial2Components = trial2.components
        for thisComponent in trial2.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial2" ---
        thisExp.currentRoutine = trial2
        trial2.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisLoop2, 'status') and thisLoop2.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *left_one* updates
            
            # if left_one is starting this frame...
            if left_one.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                left_one.frameNStart = frameN  # exact frame index
                left_one.tStart = t  # local t and not account for scr refresh
                left_one.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(left_one, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'left_one.started')
                # update status
                left_one.status = STARTED
                left_one.setAutoDraw(True)
            
            # if left_one is active this frame...
            if left_one.status == STARTED:
                # update params
                pass
            
            # if left_one is stopping this frame...
            if left_one.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > left_one.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    left_one.tStop = t  # not accounting for scr refresh
                    left_one.tStopRefresh = tThisFlipGlobal  # on global time
                    left_one.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'left_one.stopped')
                    # update status
                    left_one.status = FINISHED
                    left_one.setAutoDraw(False)
            
            # *right_one* updates
            
            # if right_one is starting this frame...
            if right_one.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                right_one.frameNStart = frameN  # exact frame index
                right_one.tStart = t  # local t and not account for scr refresh
                right_one.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(right_one, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'right_one.started')
                # update status
                right_one.status = STARTED
                right_one.setAutoDraw(True)
            
            # if right_one is active this frame...
            if right_one.status == STARTED:
                # update params
                pass
            
            # if right_one is stopping this frame...
            if right_one.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > right_one.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    right_one.tStop = t  # not accounting for scr refresh
                    right_one.tStopRefresh = tThisFlipGlobal  # on global time
                    right_one.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'right_one.stopped')
                    # update status
                    right_one.status = FINISHED
                    right_one.setAutoDraw(False)
            
            # *textbox_to_prompt* updates
            
            # if textbox_to_prompt is starting this frame...
            if textbox_to_prompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                textbox_to_prompt.frameNStart = frameN  # exact frame index
                textbox_to_prompt.tStart = t  # local t and not account for scr refresh
                textbox_to_prompt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(textbox_to_prompt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'textbox_to_prompt.started')
                # update status
                textbox_to_prompt.status = STARTED
                textbox_to_prompt.setAutoDraw(True)
            
            # if textbox_to_prompt is active this frame...
            if textbox_to_prompt.status == STARTED:
                # update params
                pass
            
            # if textbox_to_prompt is stopping this frame...
            if textbox_to_prompt.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > textbox_to_prompt.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    textbox_to_prompt.tStop = t  # not accounting for scr refresh
                    textbox_to_prompt.tStopRefresh = tThisFlipGlobal  # on global time
                    textbox_to_prompt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'textbox_to_prompt.stopped')
                    # update status
                    textbox_to_prompt.status = FINISHED
                    textbox_to_prompt.setAutoDraw(False)
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            
            # if key_resp is stopping this frame...
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.tStopRefresh = tThisFlipGlobal  # on global time
                    key_resp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp.stopped')
                    # update status
                    key_resp.status = FINISHED
                    key_resp.status = FINISHED
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
                    # was this correct?
                    if (key_resp.keys == str(cor_pass)) or (key_resp.keys == cor_pass):
                        key_resp.corr = 1
                    else:
                        key_resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=trial2,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                trial2.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if trial2.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in trial2.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial2" ---
        for thisComponent in trial2.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial2
        trial2.tStop = globalClock.getTime(format='float')
        trial2.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial2.stopped', trial2.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
            # was no response the correct answer?!
            if str(cor_pass).lower() == 'none':
               key_resp.corr = 1;  # correct non-response
            else:
               key_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for loop2 (TrialHandler)
        loop2.addData('key_resp.keys',key_resp.keys)
        loop2.addData('key_resp.corr', key_resp.corr)
        if key_resp.keys != None:  # we had a response
            loop2.addData('key_resp.rt', key_resp.rt)
            loop2.addData('key_resp.duration', key_resp.duration)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if trial2.maxDurationReached:
            routineTimer.addTime(-trial2.maxDuration)
        elif trial2.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "feedback_tesst2" ---
        # create an object to store info about Routine feedback_tesst2
        feedback_tesst2 = data.Routine(
            name='feedback_tesst2',
            components=[feedback_test2],
        )
        feedback_tesst2.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_2
        if key_resp.corr==1:
            feedback2="选对了"
        else:
            feedback2="选错了"
        feedback_test2.setText(feedback2)
        # store start times for feedback_tesst2
        feedback_tesst2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        feedback_tesst2.tStart = globalClock.getTime(format='float')
        feedback_tesst2.status = STARTED
        thisExp.addData('feedback_tesst2.started', feedback_tesst2.tStart)
        feedback_tesst2.maxDuration = None
        # keep track of which components have finished
        feedback_tesst2Components = feedback_tesst2.components
        for thisComponent in feedback_tesst2.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "feedback_tesst2" ---
        thisExp.currentRoutine = feedback_tesst2
        feedback_tesst2.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisLoop2, 'status') and thisLoop2.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *feedback_test2* updates
            
            # if feedback_test2 is starting this frame...
            if feedback_test2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                feedback_test2.frameNStart = frameN  # exact frame index
                feedback_test2.tStart = t  # local t and not account for scr refresh
                feedback_test2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(feedback_test2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'feedback_test2.started')
                # update status
                feedback_test2.status = STARTED
                feedback_test2.setAutoDraw(True)
            
            # if feedback_test2 is active this frame...
            if feedback_test2.status == STARTED:
                # update params
                pass
            
            # if feedback_test2 is stopping this frame...
            if feedback_test2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > feedback_test2.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    feedback_test2.tStop = t  # not accounting for scr refresh
                    feedback_test2.tStopRefresh = tThisFlipGlobal  # on global time
                    feedback_test2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'feedback_test2.stopped')
                    # update status
                    feedback_test2.status = FINISHED
                    feedback_test2.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=feedback_tesst2,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                feedback_tesst2.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if feedback_tesst2.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in feedback_tesst2.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "feedback_tesst2" ---
        for thisComponent in feedback_tesst2.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for feedback_tesst2
        feedback_tesst2.tStop = globalClock.getTime(format='float')
        feedback_tesst2.tStopRefresh = tThisFlipGlobal
        thisExp.addData('feedback_tesst2.stopped', feedback_tesst2.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if feedback_tesst2.maxDurationReached:
            routineTimer.addTime(-feedback_tesst2.maxDuration)
        elif feedback_tesst2.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        # mark thisLoop2 as finished
        if hasattr(thisLoop2, 'status'):
            thisLoop2.status = FINISHED
        # if awaiting a pause, pause now
        if loop2.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            loop2.status = STARTED
        thisExp.nextEntry()
        
    # completed 3 repeats of 'loop2'
    loop2.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "endtest" ---
    # create an object to store info about Routine endtest
    endtest = data.Routine(
        name='endtest',
        components=[endtest_text],
    )
    endtest.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for endtest
    endtest.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    endtest.tStart = globalClock.getTime(format='float')
    endtest.status = STARTED
    thisExp.addData('endtest.started', endtest.tStart)
    endtest.maxDuration = None
    # keep track of which components have finished
    endtestComponents = endtest.components
    for thisComponent in endtest.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "endtest" ---
    thisExp.currentRoutine = endtest
    endtest.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *endtest_text* updates
        
        # if endtest_text is starting this frame...
        if endtest_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            endtest_text.frameNStart = frameN  # exact frame index
            endtest_text.tStart = t  # local t and not account for scr refresh
            endtest_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(endtest_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'endtest_text.started')
            # update status
            endtest_text.status = STARTED
            endtest_text.setAutoDraw(True)
        
        # if endtest_text is active this frame...
        if endtest_text.status == STARTED:
            # update params
            pass
        
        # if endtest_text is stopping this frame...
        if endtest_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > endtest_text.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                endtest_text.tStop = t  # not accounting for scr refresh
                endtest_text.tStopRefresh = tThisFlipGlobal  # on global time
                endtest_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'endtest_text.stopped')
                # update status
                endtest_text.status = FINISHED
                endtest_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=endtest,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            endtest.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if endtest.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in endtest.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "endtest" ---
    for thisComponent in endtest.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for endtest
    endtest.tStop = globalClock.getTime(format='float')
    endtest.tStopRefresh = tThisFlipGlobal
    thisExp.addData('endtest.stopped', endtest.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if endtest.maxDurationReached:
        routineTimer.addTime(-endtest.maxDuration)
    elif endtest.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    # stop any playback components
    if thisExp.currentRoutine is not None:
        for comp in thisExp.currentRoutine.getPlaybackComponents():
            comp.stop()
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
