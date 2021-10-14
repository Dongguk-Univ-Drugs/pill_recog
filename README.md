<darknet 사용시>
cpu=1, cv=1 을 이용하여 빌드하기 때문에 
LIBSO=1 으로 해야 python 모듈 사용 가능

Dockerfile.base 를 이용해 base image 생성


docker build -t dgu_pill_recog .

docker run -it --rm --volume="$(PWD):/app" dgu_pill_recog
# docker run -it --rm --volume="$(PWD):/app" dgu_pill_recog bash bash로 들어가고 싶은 경우


base 빌드시 pytesseract가 설치되지 않는 이슈가 있음.