# coding=utf-8
import os
import argparse

import Foundation
from AppKit import NSImage
import objc

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

ICON_PATH = 'web_develop/chapter14/section5'


def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={},
           is_error=False):
    icon = NSImage.alloc().initByReferencingFile_(
        os.path.join(ICON_PATH, 'douban.png'))

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    notification.set_identityImage_(icon)
    if is_error:
        error_image = NSImage.alloc().initByReferencingFile_(
            os.path.join(ICON_PATH, 'error.png'))
        notification.setContentImage_(error_image)
    if sound:
        notification.setSoundName_('NSUserNotificationDefaultSoundName')

    notification.setDeliveryDate_(
        Foundation.NSDate.dateWithTimeInterval_sinceDate_(
            delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter(
    ).scheduleNotification_(notification)


def main():
    unicode = lambda s: s.decode('utf-8')
    parser = argparse.ArgumentParser(
        description='Send a custom notification on OS X.')
    parser.add_argument('-t', '--title', help='title of notification',
                        default='', type=unicode)
    parser.add_argument('-s', '--subtitle', help='subtitle of notification',
                        default='', type=unicode)
    parser.add_argument('-m', '--message', help='message of notification',
                        default='', type=unicode)
    parser.add_argument('--sound', help='include audible alert',
                        action='store_true', default=True)
    parser.add_argument('--error', help='this is a error message',
                        action='store_true', default=False)
    args = parser.parse_args()
    notify(args.title, args.subtitle,
           args.message, sound=args.sound, is_error=args.error)

if __name__ == '__main__':
    main()
