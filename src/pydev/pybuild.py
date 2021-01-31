import os
import cv2
import shutil
import time

# ----- pug file set -----
pugPath = '../pydist/_buildImg.pug'
pugImgCodeFirst = 'img(src=`${imgPath}'
pugImgCodeLast = ' alt="")'
if os.path.exists(pugPath):
    os.remove(pugPath)
with open(pugPath, mode='a') as f:
    f.write('mixin buildImg\n')

# ----- sass file set -----
sassPath = '../pydist/_buildImg.sass'
# imgSet.sassファイルの初期化
if os.path.exists(sassPath):
    os.remove(sassPath)
with open(sassPath, mode='a') as f:
    f.write('@mixin buildImg\n')


# ----- other file set -----
indent = '  '
indent2 = '    '
indent3 = '      '

# ----- python set -----
imgPath = '../../dist/img/'  # 書き出し先
inputImgPath = 'img/'  # 読み込み先
print(os.path.exists(imgPath))
if os.path.exists(imgPath):
    shutil.rmtree(imgPath)
    time.sleep(1)
    shutil.copytree(inputImgPath, imgPath)
else:
    shutil.copytree(inputImgPath, imgPath)

def creatPug(fileN, fileD, className):
    with open(pugPath, mode='a') as f:
        f.write(
            indent + '.' + className + '\n' +
            indent2 + pugImgCodeFirst + fileN + '`,' +
            ' width="' + str(fileD[fileN]['w']) + '", height="' + str(fileD[fileN]['h']) + '",' +
            pugImgCodeLast + '\n')
    return


def creatSass(fileN, fileD, className):
    with open(sassPath, mode='a') as f:
        f.write(
            '.' + className + '\n' +
            indent + 'img' + '\n' +
            indent2 + 'width: px_to_vw(' + str(fileD[fileN]['w']) + ')\n' +
            indent2 + 'max-width: px_to_rem(' + str(fileD[fileN]['w']) + ')\n' +
            indent2 + 'height: px_to_vw(' + str(fileD[fileN]['h']) + ')\n' +
            indent2 + 'max-height: px_to_rem(' + str(fileD[fileN]['h']) + ')\n')
    return


# ----- main function -----
for filename in os.listdir(imgPath):
    isFile = os.path.isfile(os.path.join(imgPath, filename))
    if isFile:
        # ゴミファイル避け
        if filename != '.DS_Store':
            im = imgPath + filename
            # ファイル名と拡張子を分けて取得, gif以外を処理
            base, ext = os.path.splitext(filename)

            if ext != '.gif':
                # 画像から幅・高さを取得、格納
                cvGetimage = cv2.imread(im)
                height, width, _ = cvGetimage.shape
                filesDetails = {filename: {'w': width, 'h': height}}

                # ファイル生成
                creatPug(filename, filesDetails, base)
                creatSass(filename, filesDetails, base)

            elif ext == '.gif':
                # 例外処理されたファイルを出力（確認用）
                print(filename)

        else:
            # 例外処理されたファイルを出力（確認用）
            print(filename)
