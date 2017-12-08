GITHUB_ORG_NAME :=

include ./env.mk

.PHONY: circleci-add-project
circleci-add-project:
	open https://circleci.com/add-projects/gh/$(GITHUB_ORG_NAME)
