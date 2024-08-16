main:
	mkdir -p build
	cd build && cmake .. && make

clean:
	rm build -rf
	rm __pycache__ -rf
	rm detect
