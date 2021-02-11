#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

const char* word_alphabet = "abcdefghijklmnopqrstuvwxyz";
const auto is_char_illegal = [](char c) -> bool {
  for (size_t i = 0; i < std::strlen(word_alphabet); i++) {
    if (word_alphabet[i] == c) return false;
  }
  return true;
};

// using name_t = std::pair<float, std::string>;
using name_t = std::pair<int, std::string>;
const auto name_t_sort = [](const name_t& lhs, const name_t& rhs) -> bool {
  if (lhs.first != rhs.first) {
    return lhs.first < rhs.first;
  } else {
    return lhs.second.compare(rhs.second) < 0;
  }
};

int main(int argc, char *argv[]) {
  if (argc != 2) {
    std::cout << "Invalid number of arguments. Specify log file." << std::endl;
  }
  const auto log_file = argv[1];

  std::vector<std::string> words;
  {
    std::ifstream dict("/usr/share/hunspell/en_US.dic");
    std::string word;
    std::getline(dict, word);
    words.reserve(std::atoi(word.c_str()));
    words.push_back("is");
    words.push_back("of");
    words.push_back("to");
    while (std::getline(dict, word)) {
      word = std::string(word.begin(), std::find(word.begin(), word.end(), '/'));
      std::transform(word.begin(), word.end(), word.begin(), [] (uint8_t c) { return std::tolower(c); });
      if ((word.length() >= 3) && std::find_if(word.begin(), word.end(), is_char_illegal) == word.end()) {
        words.push_back(std::move(word));
      }
    }

    std::sort(words.begin(), words.end(), [](const std::string& lhs, const std::string& rhs) {
      return lhs.compare(rhs) < 0;
    });
    auto new_last = std::unique(words.begin(), words.end());
    words.erase(new_last, words.end());
  }

  std::vector<name_t> names;
  {
    std::ifstream log(log_file);
    std::string name;
    while(std::getline(log, name)) {
      const char* flag = "  Solved: ";
      auto i = name.rfind(flag, 2);
      if (i == 0 || i == 2) {
        names.push_back(std::make_pair(0, name.substr(std::strlen(flag) + i)));
      }
    }
  }

  for (auto& name: names) {
    for (auto& word: words) {
      auto p = name.second.find(word);
      while (p != std::string::npos) {
        auto beg = p == 0;                                          // match at beginning
        auto end = p == (name.second.length() - word.length());     // match at end
        auto left_ = beg || name.second[p - 1] == '_';              // '_' left of match or start
        auto right_ = end || name.second[p + word.length()] == '_'; // '_' right of match or end
        if (left_ || right_) {
          name.first += (left_ && right_ ? 2 : 1) * 50 * word.length();
        } else {
          name.first += 1 * word.length();
        }
        p = name.second.find(word, p + word.length());
      }
      // name.first /= name.second.length();
    }
  }

  std::sort(names.begin(), names.end(), name_t_sort);

  for (auto& name: names) {
    std::cout.width(6);
    std::cout << name.first << " " << name.second << std::endl;
  }
}
