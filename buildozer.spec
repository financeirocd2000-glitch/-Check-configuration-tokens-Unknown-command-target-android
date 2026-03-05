[app]
title = Coletor
package.name = coletor
package.domain = org.coletor

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0
requirements = python3,kivy,opencv,pyzbar,plyer

orientation = portrait
fullscreen = 0

# ANDROID
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
