RUYI_TARGET = ruyi.css
RUYI_SOURCES = \
	normalize.css \
	skeleton.css \
	animation.css \
	ruyi/ruyi.sass.css \
	jvm.css \
	lity.css \
	syntax.css \

.PHONY: all
all: ../static/css/$(RUYI_TARGET)

../static/css/$(RUYI_TARGET): $(RUYI_TARGET)
	mkdir -p ../static/css
	cat $(RUYI_TARGET) | sed 's/\/\*!/\/**/g' | yui-compressor --type css > ../static/css/$(RUYI_TARGET)

$(RUYI_TARGET): $(RUYI_SOURCES) $(shell find opensans/ -type f -print)
	( ./opensans/opensans.bash; cat $(RUYI_SOURCES) ) > $(RUYI_TARGET)

%.sass.css: %.sass $(shell find . -type f -iname _\*.sass)
	cat $< | sass --compass --load-path . > $<.css

.PHONY: clean
clean:
	find . -iname \*.sass.css -exec rm -f {} \;
	rm -rf .sass-cache
	rm -f $(RUYI_TARGET)
	rm -f ../static/css/$(RUYI_TARGET)

