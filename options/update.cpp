#include <iostream>
#include <string>
#include <fstream>
#include <vector>

using namespace std;

int main(int argc, char *argv[]) {
    ofstream file("blacklist.txt", ios_base::app);

    if (!file.is_open()) {
        cout << "Error: Could not open file blacklist.txt" << endl;
        return 1;
    }

    //ex: ./update blacklist 45
    //ex: ./update 
    if (argc == 1)
    {
        cout << "Commands: " << endl;
        cout << "blacklist <number>" << endl;
        cout << "whitelist <number>" << endl;
    }

    else if (argc != 3)
    {
        cout << "Error: Invalid number of arguments" << endl;
        return 1;
    }

    else 
    {
        string option = argv[1];
        string value = argv[2];

        if (option == "blacklist")
        {
            file <<  value << endl;
        }

        else if (option == "whitelist")
        {
            ifstream infile("blacklist.txt");
            if (!infile.is_open())
            {
                cout << "Error: Could not open file options.cfg" << endl;
                return 1;
            }

            vector<string> lines;
            string line;
            while (getline(infile, line))
            {
                if (line.find(value) == string::npos)
                {
                    lines.push_back(line);
                }
            }

            infile.close();

            ofstream outfile("blacklist.txt");
            if (!outfile.is_open())
            {
                cout << "Error: Could not open file options.cfg" << endl;
                return 1;
            }

            for (string line : lines)
            {
                outfile << line << endl;
            }

            outfile.close();
            cout << "Printer " << value << " removed from blacklist" << endl;
        }

        else 
        {
            cout << "Error: Invalid option" << endl;
            return 1;
        }
    }

    file.close();
    return 0;
    

} 