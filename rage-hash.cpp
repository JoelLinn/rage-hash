#include <iostream>
#include <string>
#include <string_view>

using hash_t = uint32_t;

hash_t hash_name(std::string_view name) {
	hash_t hash = 0;
	for (auto c : name)
	{
        hash += c;
        hash += hash << 10;
        hash ^= hash >> 6;
    }
    hash += hash << 3;
    hash ^= hash >> 11;
    return (hash + (hash << 15));
}

void first(std::string& name, size_t len) {
    name.resize(len, 'a');
}

bool next(std::string& name) {
    //const char* charset = "abcdefghijklmnopqrstuvwxyz_";
    for (auto& c : name)
    {
        if (c == '_') {
            // overflow
            c = 'a';
            continue;
        }
        if (++c > 'z') {
            c = '_';
        }
        return true;
	}
    return false;
}


int main(int argc, char *argv[])
{
    std::cout << "Thanks to xSonoro & XeClutch for their work." << std::endl << std::endl;

    if (argc == 2) {
        std::cout << "0x" << std::hex << hash_name(argv[1]) << std::dec << std::endl;
    } else if (argc == 4) {
        hash_t hash = static_cast<hash_t>(strtoll(argv[1], nullptr, 16));
        auto len_min = atoi(argv[2]);
        auto len_max = atoi(argv[3]);
        std::cout << "Started solving hash: 0x" << std::hex << hash << std::dec << std::endl;

        for (auto i = len_min; i <= len_max; i++)
        {
            std::cout << "  Length: " << i << std::endl;

            std::string name;
            first(name, i);
            do {
                if (hash_name(name) == hash) {
                    std::cout << "    Solved: " << name << std::endl;
                }
            } while(next(name));
        }
        std::cout << "Done. Terminating." << std::endl;
    } else {
        std::cout << "Invalid arguments." << std::endl;
    }

	return 0;
}
