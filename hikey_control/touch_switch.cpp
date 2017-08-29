#include <string>
#include <unistd.h>
#include "mraa.hpp"

int main(int argc, char* argv[])
{
    if (argc != 2) {
	return 1;
    }

    std::string new_state = argv[1];

    mraa::Gpio* relay_gpio = new mraa::Gpio(27);
    mraa::Result response;

    response = relay_gpio->dir(mraa::DIR_OUT);
    if (response != mraa::SUCCESS) {
        return 1;
    }
    
    if (new_state == "on") {
        relay_gpio->write(true);
    } else {
        relay_gpio->write(false);
    }

    delete relay_gpio;
    return response;
}
