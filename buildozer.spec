# (str) Title of your application
[app]

title = FOULOLOU MILOUD'S RIVAL CENTIPEDE
package.name = foulouloucentipede
package.domain = org.fouloulou

source.dir = .
source.include_exts = py,txt,mp3,wav,ogg
version = 1.0

requirements = python3,pygame-ce,plyer

orientation = portrait
fullscreen = 1

android.archs = arm64-v8a
android.minapi = 24
android.api = 36
android.ndk = 29
android.permissions = VIBRATE

p4a.bootstrap = sdl2
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
