ENV_MK := ./env.mk

GITHUB_ORG_NAME :=
GITHUB_REPO_NAME :=
GITHUB_REPO :=
CIRCLECI_TOKEN :=

include $(ENV_MK)

CIRCLECLI := python $(CURDIR)/scripts/circlecli.py --token $(CIRCLECI_TOKEN)


.PHONY: setup-circleci-project
setup-circleci-project:
	@# CirleCIのprojectをenableにする
	open https://circleci.com/add-projects/gh/$(GITHUB_ORG_NAME)


.PHONY: setup-circleci-token
setup-circleci-token:
	@# CirleCIのAPI Tokenを作成する
	@if [ "$(CIRCLECI_TOKEN)" ] ; then \
		echo "Already setup CIRCLECI_TOKEN."; \
	else \
		open https://circleci.com/gh/$(GITHUB_REPO)/edit#api; \
		echo "Edit CIRCLECI_TOKEN: $(ENV_MK)"; \
	fi


.PHONY: circleci-get-environ
circleci-get-environ:
	@# CircleCIの環境変数を表示します。
	$(CIRCLECLI) show


.PHONY: circleci-reset-environ
circleci-reset-environ:
	@# CircleCIの環境変数を全て削除します。
	$(CIRCLECLI) reset


.PHONY: circleci-apply-environ
circleci-apply-environ:
	@# CircleCIの環境変数を反映します。
	$(CIRCLECLI) apply


.PHONY: build
build:
	@# ビルドします。
	yarn build

.PHONY: s3-upload
s3-upload:
	@# s3にファイルをuploadします。
	aws s3 sync ./build s3://sximada-aws-static-files/ --acl public-read --profile aws-static-files
