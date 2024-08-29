# Database_Difference_Checker-Python_SQLite
Python script to read SQLite files and check the differences between them.

## Before you start!
This document provides a step-by-step guide to performing comparison between SQLite databases using the `Database_Difference_Checker-Python_SQLite` script.

## Instructions for Use
### 1. Using filters for tables and/or columns _(Optional Step)_
- **Table Filters**: Edit the `constants/general.py` file and add the names of the tables you want to exclude from the comparison within the `EXCLUDED_TABLES` constant.
  #### Example:
  ```
  EXCLUDED_TABLES = {"table1", "table2", "table3"}
  ```
- **Column Filters**: Edit the same file and add the names of the columns to be excluded from the comparison within the `EXCLUDED_COLUMNS` constant.
  #### Example:
  ```
  EXCLUDED_COLUMNS = {"column1", "column2", "column3"}
  ```

### 2. Adding SQLite databases for comparison
Place the SQLite `(.db)` files you want to compare inside the `MOCK/DATA` folder.

- For contexts of different databases _(for example, databases from different companies)_, it is ideal, but not mandatory, to organize the databases in different folders within `MOCK/DATA`.
  #### Example:
  ![image](https://github.com/user-attachments/assets/4d439483-bdcb-4bb4-aa0e-7f73a28ae0b6)

### 3. Adding the reference file
Add the file with the reference data to the `MOCK/PATTERN` folder. **The reference file can be in `.txt`, `.json`, `.sqlite` or `.db` format**.

### **Important**
- **The `.sqlite` and `.db` files take precedence over the others**
- The file must follow the pattern **_key-value_** _(key: value)_, with the **VALUE ALWAYS WRAPPED IN BRACKETS**.
  #### Examples for text file `(.txt)`:
  - **Example 1 (without line break):**
    ```
    TABLE_1:[{...}]TABLE_2:[...]TABLE_3:[...]
    ```
  - **Example 2 (with line break):**
    ```
    TABLE_1:[{...}, {...}]
    TABLE_2:[{...}]
    TABLE_3:[...]
    ```
  #### Example for JSON file `(.json)`:
  ```
  {
      "TABLE_1": [
          {
              "name": "XXXX",
              "type": "XXXX"
          },
          {
              "name": "XXXX",
              "type": "XXXX"
          }
      ],
      "TABLE_2": [
          {
              "name": "XXXX",
              "type": "XXXX"
          }
      ],
      ...
  }
  ```

### 4. Analysis of Results
After executing the script, check the `trackingCode`. The code `00` indicates that the process completed without errors (other tracking codes in the section below).

**The comparison results will be saved in a JSON file in the project root folder, called `Output.json` .**

#### Example of `Output.json` file:
```
{
    "MAIN_DATABASE_1": {
        "DATABASE_SQLite_1": {
            "Missing_Tables": [...],
            "Missing_Data": {
                "TABLE_1": [
                {
                    "name": "XXXX",
                    "type": "XXXX"
                }
                ],
                "TABLE_2": [...]
            }
        },
        "DATABASE_SQLite_2": {...}
    },
    "MAIN_DATABASE_2": {...}
}
```

## Tracking Codes

Tracking codes indicate the status of the process:

- `00`: **Finished without errors**
- `01`: **An unexpected error occurred**
- `02`: **Error reading file(s)**
- `03`: **Error reading file(s) from directory**
- `04`: **Error in the comparison process**
- `05`: **Error generating `Output.json` file**
- `06`: **Error reading data from databases**
- `07`: **Error generating JSON from databases**
- `08`: **Error when fetching JSON files from databases**
- `09`: **Error creating reference JSON**
- `10`: **Invalid file extension**

## 🛠 Used Packages

| Name      | Version |
| :-------- | :------ |
| 🐍 Python | `3.8.0` |

## 🔗 Links

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GabrielTorelo/Database_Difference_Checker-Python_SQLite)
