# warrobots-player-stats

Analysis of player statistics in the mobile app game 'War Robots'. The data is acquired from game screenshots and OCR in python. The analysis reveals the most popular and possibly best in-game equipment.

### Installation
```
$ git clone https://github.com/andibarg/warrobots-player-stats.git
$ cd warrobots-player-stats
```
Required python 3 packages: os, matplotlib, numpy, opencv, pytesseract, pandas, re, tqdm.

### Usage

The script '1_run_ocr.py' acquires data via OCR (pytesseract) from in-game screenshots of player statistics. These screenshots are stored in a subfolder under '/data'. As an example, 97 screenshots of Legend League players taken on 2019-01-16 are included. To run '1_run_ocr.py' you first have to specify the subfolder that includes the screenshots. The script crops the screenshots tightly around text labels whose coordinates are given in the file 'other/text_pos.csv' (use 'show_screenshot=True' to see whay is going on). Subsequently, the OCR is run. If 'savetofile=True', all OCR outputs are saved as a csv file in '/data'. You might want to check the csv file while running '1_run_ocr.py' to see if things work properly.

The following figure shows what you might see when you run '1_run_ocr.py'. The white rectangle indicates the label currently read by the OCR. On the right a preview of the csv file generated by the script is shown.

![Screenshot](other/ocr_running_example.png)

As a second step, open '2_analyze_ocr.py' and specify the name of the csv file including the OCR outputs. Afterwards, you can run the script. It will first try to clean the dataframe by identifying the 'MK2' labels and by going through the equipment list provided in the file 'other/equip_list.csv'. Note that regular expressions are used, mostly to correct the fact that the OCR often confuses the letters 'o' and 'a'. The cleaned data frame is saved as a csv file in the folder '/plots' together with the plots generated by the analysis.

### Examples

The following two figures show overviews of robots and weapons most commonly used by the top 100 players (Legend League). The white and green bars indicate the MK1 and MK2 equipment, respectively.

![Screenshot](plots/iOS_LL_2019-01-16/Robots.png)
![Screenshot](plots/iOS_LL_2019-01-16/Weapons.png)

Let us look at all the weapons used for each robot individually. For the most common robot 'Ares', for instance, we get the list of weapons shown below.

![Screenshot](plots/iOS_LL_2019-01-16/Ares.png)


### Suggestions for improvements

- Read out more data from the screenshots such as player ID, rating, and percentage of victories.
- Account for multiple hangars per player.
- Collect new data every month to observe how the numbers change over time, specifically after buffs and nerfs.
- Include data from other plattforms.
