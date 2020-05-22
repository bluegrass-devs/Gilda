.DEFAULT_GOAL := none

.PHONY: none
none:
	@printf "there is no default make target. try\\n* check\n\n"

DOCKER := $(shell which docker)
FN := $(shell which fn)

.PHONY: check
check:
	@[ -n "${DOCKER}" ] || (echo "missing docker" && exit 1)
	@echo "docker: installed at ${DOCKER}"
	@[ -n "${FN}" ] || (echo "missing fn" && exit 1)
	@echo "fn: installed at ${FN}"
	@$(DOCKER) ps -q > /dev/null || (echo "docker cant reach server" ; exit 1)
	@echo "docker-host: running"
	@[ $$(${FN} version | grep --count ?) == 0 ] || (echo "fn server not running" && exit 1)
	@echo "fn-server: running"
	@set -o errexit ; for config in webhook_url random_channel_id ; do \
		${FN} get config app gilda $$config > /dev/null 2>&1 || \
		    (echo "gilda app config incomplete" && exit 1) ; \
	done
	@echo gilda-app: configured
	@echo ALL PRE-FLIGHT CHECKS PASSED, HAPPY HACKING
