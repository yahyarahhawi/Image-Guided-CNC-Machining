
# Image-Guided-CNC-Machining Using Intersection-over-union and edge detection

This project is focused on investigating image processing methods to enhance visual monitoring systems in CNC machining and manufacturing environments. It addresses two main challenges: dimensional variations and visual defects. To tackle these issues, the project employs techniques such as Intersection-over-Union for measuring dimensional changes and edge detection algorithms for identifying visual flaws.




## Acknowledgements
 - Professor Andrea Vaccari for his assistance throughout the project!




## Authors

- [@yahyarahhawi](https://www.github.com/yahyarahhawi)


## Deployment

To deploy this project, connect a webcam and prepare a scene where parts are placed at a specific position, lit by a background light for segmentation. Refer to example images in jupyter notebook

```bash
  run Webcam Live.py
```


## Intoduction
About a year ago, I had the great experience of working at a CNC industrial manufacturing shop focused on producing high-precision parts for medical devices. It was during this period that I was amazed by the precision that CNC machines can achieve. Despite their remarkable capabilities, even the slightest deviations, such as those caused by tool wear, could lead to parts that failed to meet specifications. This challenge made me interested in exploring how various algorithms could be integrated into the manufacturing process to enhance efficiency, particularly through automation.

Motivated by my experiences last summer, I started this project as a part of my CS0452 image processing class. The primary goal of this project is to address two critical issues that frequently affected the quality of the parts we produced: dimensional errors and visual defects. Dimensional errors, or deviations from the specified geometrical precision, can render parts unusable. Visual flaws, such as scratches, dents, or discoloration, also significantly impact the usability and aesthetic quality of the manufactured items.

Throughout this semester in CS0452, I've acquired a range of tools and techniques in the field of image processing that I believe can be effectively applied to these manufacturing challenges. This project utilizes Intersection-over-Union (IoU) to quantitatively assess dimensional changes and employs edge detection algorithms to identify and classify visual defects. By applying these image processing techniques, I aim to demonstrate how the integration of these computational methods can significantly mitigate common manufacturing issues, leading to better product quality and increased operational efficiency.

I invite you to explore the code, offer suggestions, and contribute to enhancing how CNC manufacturing can benefit from the intersection of computer science and industrial engineering. Thank you for visiting, and I look forward to collaborating with you on this journey to bridge the gap between theoretical knowledge and practical industrial application.








## Intersection over Union (IoU)
**Intersection over Union (IoU)** is a powerful technique utilized to quantify dimensional errors in manufactured parts, especially useful in precision-dependent fields like CNC machining. Here's a detailed step-by-step description of how the IoU is applied to evaluate the conformity of manufactured parts to their designated templates:

**Overview of Process**

1. **Template and Part Representation:**

Template: This is a digital or visual representation of the ideal dimensions and shape of the part that needs to be manufactured. It serves as the standard or goal for production.
Part to be Measured: After manufacturing, the actual part produced is assessed to ensure it matches the dimensions and shape of the template.

2. **Color Coding for Visualization:**

Each component, the template and the actual part, is given a distinct color. This visual differentiation aids in clearly identifying the areas of overlap and the areas where discrepancies occur between the template and the manufactured part.
Intersection and Union Analysis:

3. **Intersection:**
This is determined by identifying the common area where both the template and the manufactured part overlap. The intersection area is crucial for understanding the extent to which the part matches the template.

4. **Union:** This includes all the areas covered by either the template or the manufactured part, encompassing any space that either occupies.

5. **Calculation of IoU**: The IoU metric is calculated by dividing the area of intersection by the area of union. This ratio provides a numerical value that represents the degree of conformity of the manufactured part to the template. A higher IoU value means that better conformity, while a lower IoU means greater deviation.

**Practical Application**
The application of IoU in manufacturing settings, particularly where precision is very important, allows for a quantitative examination of whether parts conforms to drawing measurements or not. This metric helps in identifying whether the manufactured parts are within the acceptable tolerance limits required for their specific applications. It serves as a critical quality control measure, ensuring that each part produced meets stringent specifications and reducing the risk of errors that could impact the final product's functionality.



## Visual defects
**Visual defects**

this flowchart was used:
![Screenshot (310)](https://github.com/yahyarahhawi/Image-Guided-CNC-Machining/assets/170378585/05abdb1c-8809-4259-b9e7-3442dc222434)


**Base Image**: This is the reference image, presumably of the part as it should ideally appear without any defects.

**Measured Image**: This image is of the actual manufactured part being inspected.

**Segmentation:**
Both the base image and the measured image undergo a segmentation process. Segmentation is used to isolate the part from the background, simplifying further analysis by focusing only on the regions of interest, which are the parts themselves.

**Enhance Details:**
The segmented measured image is processed to enhance details. This is typically done through techniques such as gamma correction and histogram equalization. Gamma correction adjusts the luminance of the image, and histogram equalization improves the contrast, making defects more visible.

**Thresholded Sobel Edge Detection:**
After enhancing the details of the image, a Sobel edge detector is applied. This operator helps in detecting edges in the image based on intensity gradients. The output is likely thresholded to ignore less significant edges, focusing only on prominent features which could indicate defects.

**Canny Edge Detection:**
The segmented base image undergoes Canny edge detection, another method of edge detection that detects a wide range of edges in images. Canny edge detection is known for its effectiveness in accurately detecting edges.

**Subtract and Analyze:**
The final step involves subtracting the edge-detected measured image from the edge-detected base image. This subtraction highlights the differences between the expected edges (from the base image) and the actual edges (from the measured image).
The differences are analyzed by calculating the ratio of the subtracted white pixels (which represent discrepancies or defects) to the total number of pixels in the segmentation mask of the base image. This ratio quantifies the extent of aesthetic errors or defects.
## Demo

![demo](https://github.com/yahyarahhawi/Image-Guided-CNC-Machining/assets/170378585/3b948041-5b4d-4465-aefa-3cc5d0063078)



## Results
As seen in the demo, the program successfully highlights areas where the parts differ in dimensions and where defects exist. The webcam version allows for a live preview of the parts and monitors the changes that these parts undergo over time. The user interface provides simple controls for threshold values and to adjust the webcam exposure and focus (they must be adjustable in the first place. The logitech camera I was using allowed for manual controls). In addition to the demo, you can preview the jupyter notebook which showcases how these two algorithms are used on two example images. The project expects an easily-thresholded images of the parts (I used an Ipad to produce backlight) and then all you do is capturing a base image, changing the parts, and calculating dimensional errors and detect flaws.  

The project has the following shortcomings:
1. due to the reflective nature of metal (believe it or not), It becomes very hard to segment it as it reflects lights from the surrounding and contains bright spots that gets segmented away, and it also causes an issue of these reflections being recognized as flaws similar to scratches on the metal parts. The following area represents a flaw, while it is simply a reflection that is seen accross all parts.

![Screenshot 2024-05-20 224315](https://github.com/yahyarahhawi/Image-Guided-CNC-Machining/assets/170378585/ee2ae213-030f-4b54-9de6-21406d1e464e)


2. Both algorithms assumet hat parts are constantly placed in the same position to do the comparasion. This is typically not always correct since this comes with its own certaintiy and precision. 

3. The project focused on finding dimensional changes of parts that have very clear and distinct edges. The project fails to deal with parts with higher edge density and with more organic shapes. Where do we define edges with an organic form?

A potential **solutions** to all these problems include:
1. better algorithm for segmentation. Maybe machine learning or green screen?
2. rely on robotic arms for placements of parts which significantly increases precision.
3. develop a more customizable interface that allows the user to use different edge detection methods or threshold levels that accommodate different forms of parts.



## Accessibility 
Accessibility Considerations for the project

1. **Color Blindness:**
Choosing appropriate colors is crucial for making this  project accessible to individuals with color vision deficiencies. To improve accessibility for users with color blindness, I can utilize color palettes that are distinguishable to all users, including those who are color blind. Implementing color schemes, specifically for visualizing the intersection over union, that differentiate through brightness and saturation, in addition to hue, can help in making visual elements clear and distinguishable.

2. **Manual handling:**
Our application currently requires precise manual interaction, which might not be suitable for users with limited accessibility, such as those who do not have steady hands. To enhance accessibility, I could integrate features that assist in aligning and placing parts with less reliance on manual precision. options such as a robotic arm or using template matching could assist in avoiding risky handling.

3. **Code Accessibility:**
Adjustments in the code are necessary for tailoring the application to handle different pa rts. However, not all users are able to read or understand code. To make this application more accessible, I can provide a user-friendly interface that allows non-programmers to make necessary adjustments through graphical controls or simple form-based inputs. Additionally, providing comprehensive documentation and voice-guided assistance could help users who face challenges with traditional interaction methods.

4. **Implementation of Changes:**
If possible, I should start implementing these changes to make this project more inclusive and accessible. By addressing these key areas, we can ensure that our technology is usable and beneficial to a wider range of individuals, including those with disabilities.




## Ethical implications
1. **Potential Use in Weapons Manufacturing:**
One of the pressing ethical concerns is the possibility that this algorithm can be adapted or used for use in automating the production of weapons. This application raises serious moral questions about contributing to the proliferation of arms and the potential escalation of conflicts. It is necessary to consider implementing strict usage guidelines and licensing agreements that restrict the use of the technology to non-military manufacturing sectors, which works to aligning with global peace keeping efforts.

2. **Impact on Employment:**
Another important ethical issue is the impact of automation on the workforce. While the algorithm aims to enhance efficiency and precision in manufacturing, it also presents the potential to displace workers, leading to job losses. It is imperative to approach this transition responsibly. We should advocate for and invest in retraining programs that help workers adapt to the new technology-driven landscape, ensuring that the workforce can transition to more skilled roles that support and complement the automated processes.
## Schedule
This is the proposed initial schedule:
* Line Fitting and Measurements (By April 20th):
Implement Hough Transform and edge detection for line fitting.
Develop algorithms for accurate distance, angle, and area measurements. **This milestone was met but I was not able to incooperate it effectively in the project**

* Quantifying Tool Wear Effects (By April 28th):
Develop techniques to quantify changes in part dimensions due to tool wear. **This milestone was met and played role in the IOU algorithm**

* Visualize these changes for analysis and decision-making.
Batch Processing Supervision (By May 2nd):
Implement rotation, scaling alignment, and object detection for batch processing.
Develop methods to supervise and ensure consistency across batches. **Parts of this was achieved, definitely not the ability to handle batches of parts and track down changes over time. This could be an improvement to be implemented in the future**

* Appearance Matching for 3D State Recognition (By May 16th):
Investigate advanced techniques like feature matching and deep learning for appearance matching. **This milestone was not achieved due to running out of time**

## Issues
The issues ecnountered, in addition to the ones mentioned at the results section, include:
1. I was unable to learn how to use robotic arm and demonstrate full automation of the manufacturing process of parts.
2. Due to that, a replacement to the process of the robotic arm was to 3D print a mount where parts sits on and ensures consistency in position.
3. Limited time to dedicate to the project. It was difficult to meet all the milestones I have proposed in the beginning. But this also means that future improvements are possible and I can make adjustments in the future. 
4. It was difficult to connect with the manufacturing firm I worked at and determine a time where we could meet and discuss aspects of the project. I was not able to design a product that fully meets the needs that these people have in their industry, but only the needs I remember from my short time working with them.

## Improvements
Improvements include:
1. Better segmentation method
2. use of template matching or aligning such that misplacing parts could be accounted for.
3. Impelmenting an algorithm that utilizes a changing light source (in position) that quantifies the depth of the artifacts or defects by stacking the shadows overtime. 
4. customizable settings to prevent over-fitting the algorithms to a single type of parts such as the ones used in the demonstration of the algorithm
5. better UI could definitely help! there are already a lot of bugs that produce a not very pleasing user interface.
## References
Here are the sources I used for my project. Big shout out to:
https://scikit-image.org/
https://docs.opencv.org/4.x/
https://pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
https://realpython.com/python-gui-tkinter/
https://docs.python.org/3/library/tkinter.html
