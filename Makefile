IMAGE_REPO ?= registry.cn-shanghai.aliyuncs.com/kerthcet-public/rayproject
GIT_TAG ?= $(shell git describe --tags --dirty --always)
IMAGE_WITH_TAG ?= $(IMAGE_REPO):ml-$(GIT_TAG)

.PHONY: build-aio-image
build-aio-image: build-zip
	echo $(IMAGE_WITH_TAG)
	docker buildx build \
		-f ./deploy/Dockerfile.aio \
		-t $(IMAGE_WITH_TAG) \
		--platform=linux/amd64 \
		--push \
		./ \

.PHONY: build-serving-image
build-serving-image: build-zip
	echo $(IMAGE_WITH_TAG)
	docker buildx build \
		-f ./deploy/Dockerfile.serving \
		-t $(IMAGE_WITH_TAG) \
		--platform=linux/amd64 \
		--push \
		./ \

.PHONY: zip
build-zip:
	rm -rf ./k8s-specific-knowledge-base.zip
	tar --exclude='contents/' \
		--exclude='models/' \
		--exclude='.git/' \
		-zcvf k8s-specific-knowledge-base.zip \
		./