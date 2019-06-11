DOCKER_IMAGE=nvukobrat/sinergija-diplomski
LOCAL_PROJECT_PATH=/media/nvukobrat/Data/PycharmProjects/SinergijaDiplomski/
GIT_PROJECT_PATH=~/Documents/GIT/sinergija-diplomski/Source/

init-dataset:
	rm -rf /tmp/dataset/
	mkdir /tmp/dataset/
	rsync -av --progress /media/nvukobrat/Data/Cache/SD_Dataset/SimpleCrypt/50 /tmp/dataset/
	du -hs /tmp/dataset/*

log:
	tensorboard --logdir=/tmp/log --port 6001

git-sync:
	rm -rf $(GIT_PROJECT_PATH)/
	rsync -av --progress $(LOCAL_PROJECT_PATH) $(GIT_PROJECT_PATH) --exclude venv --exclude .bash_history --exclude .python_history

docker-update:
	docker build -t $(DOCKER_IMAGE) assets/
	docker push $(DOCKER_IMAGE)