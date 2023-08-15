import os

# https://blog.csdn.net/qq_25262697/article/details/129302819
# https://www.cnblogs.com/happylee666/articles/16158458.html
os.system('nuitka --standalone --windows-disable-console --plugin-enable=pyqt5 --include-qt-plugins=sensible,styles --mingw64 --show-memory --show-progress --windows-icon-from-ico=docs/source/_static/logo.ico demo.py')
