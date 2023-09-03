# PyPointLine

PointLine is one of DGS's (Dynamic Geometry Systems), which allows users to create geometric constructions and manipulate the figure after constructing. PointLine has a 'bi-directional dependence' between geometric objects such as vertices, lines, and circles.

Let a Markov process that associates all vertexes be called a module. Modules are designed to realize geometric relationships (e.g., the midpoint of a line segment, a circle touching with a line.) We will call this the function of the module. We implement these modules as a method that makes vertices converge to those with a positional relationship such that the function of the module after we execute the process iteratively.

For example, considering a module whose function is that point C is the midpoint of line AB, we implement the following Markov process.

![中点モジュールの式](https://github.com/aharalabMeiji/PyPointLine/assets/16815591/ac7d9472-2654-46ab-86ec-40854fec7525)

We can prove that this process is a linear transformation that converges by iteration and that the limit point C is located at the midpoint of the limit line segment AB.

Let us assume that we move several such modules simultaneously. At that time, the figure may not always converge by the process. However, experiments have confirmed that it works well in many cases.

The PyPointLine project is available in Python source code. This makes it easier for researchers to study the architecture of PointLine. Project members hope to make progress in researching the mathematical properties associated with PointLine's modules.

