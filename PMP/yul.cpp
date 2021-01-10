#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

void readInclude(string);

int main(){
    string title;
    cin >> title;
    readInclude(title);
    return 0;
}

void readInclude(string title){
    ifstream bruh(title);
    if(bruh.is_open()){
        string line;
        while(getline(bruh, line)){
            if(line.find_first_of('#') != string::npos){
                readInclude(line.substr(line.find_first_of('"')+1,line.find_first_of('h')-line.find_first_of('"')));
            }
            else if(line.find_first_of('#') == string::npos){
                cout << line << endl;
            }
        }
    }
    bruh.close();
}