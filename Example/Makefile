do::
	python3 ../carify.py ./Assets ./Resources

TARGET = iphone::10.3:8.0

include $(THEOS)/makefiles/common.mk

APPLICATION_NAME = CarifyTest
CarifyTest_FILES = main.m CTAppDelegate.m CTRootViewController.m CTTabBarController.m
CarifyTest_FRAMEWORKS = UIKit CoreGraphics

include $(THEOS_MAKE_PATH)/application.mk

after-install::
	install.exec "killall \"CarifyTest\"" || true
