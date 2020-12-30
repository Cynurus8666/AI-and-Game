# Tutorials
## 1 Required tools
In order to perform experiments with Machine Learning model, it is recommended that you should have some of the following software in your check list:
- Python 3 (recommended)
- scikit-learn (better install it alone, not with anaconda)
- pandas, numpy, matplotlib, and other libraries (depends on the requirements)
- tensorflow (for deep models)
For easy interacting with the code, you can either choose Python IDEs, or Jupyter notebook (which is more convenient in this course). Python should be available on most OS, except if you are using Windows. After installing python, you need pip for installing other packages. Then it is easy to install notebook as follows:
`pip3 install  jupyter`
Then run the notebook by going to the working directory containing the notebooks and type:
`jupyter notebook`
The notebook should be available on your browser. Read here for further information on Jupyter notebook, 


# Lecture notes 
## Statistical significant test
### The Problem of Model Selection
A big part of applied machine learning is model selection.
We can describe this in its simplest form:
        `Given the evaluation of two machine learning methods on a dataset, which model do you choose?`
You choose the model with the best skill.
That is, the model whose estimated skill when making predictions on unseen data is best. This might be maximum accuracy or minimum error in the case of classification and regression problems respectively.
The challenge with selecting the model with the best skill is determining how much can you trust the estimated skill of each model. More generally:
        `Is the difference in skill between two machine learning models real, or due to a statistical chance?`
We can use statistical hypothesis testing to address this question.

### Statistical Hypothesis Tests
Generally, a statistical hypothesis test for comparing samples quantifies how likely it is to observe two data samples given the assumption that the samples have the same distribution.
The assumption of a statistical test is called the null hypothesis and we can calculate statistical measures and interpret them in order to decide whether or not to accept or reject the null hypothesis.
In the case of selecting models based on their estimated skill, we are interested to know whether there is a real or statistically significant difference between the two models.
    - If the result of the test suggests that there is insufficient evidence to reject the null hypothesis, then any observed difference in model skill is likely due to statistical chance.
    - If the result of the test suggests that there is sufficient evidence to reject the null hypothesis, then any observed difference in model skill is likely due to a difference in the models.
The results of the test are probabilistic, meaning, it is possible to correctly interpret the result and for the result to be wrong with a type I or type II error. Briefly, a false positive or false negative finding.
Comparing machine learning models via statistical significance tests imposes some expectations that in turn will impact the types of statistical tests that can be used; for example:
    - `Skill Estimate`. A specific measure of model skill must be chosen. This could be classification accuracy (a proportion) or mean absolute error (summary statistic) which will limit the type of tests that can be used.
    * `Repeated Estimates`. A sample of skill scores is required in order to calculate statistics. The repeated training and testing of a given model on the same or different data will impact the type of test that can be used.
    - `Distribution of Estimates.` The sample of skill score estimates will have a distribution, perhaps Gaussian or perhaps not. This will determine whether parametric or nonparametric tests can be used.
    - `Central Tendency.` Model skill will often be described and compared using a summary statistic such as a mean or median, depending on the distribution of skill scores. The test may or may not take this directly into account.
The results of a statistical test are often a test statistic and a p-value, both of which can be interpreted and used in the presentation of the results in order to quantify the level of confidence or significance in the difference between models. This allows stronger claims to be made as part of model selection than not using statistical hypothesis tests.
Given that using statistical hypothesis tests seems desirable as part of model selection, how do you choose a test that is suitable for your specific use case?

### Problem of Choosing a Hypothesis Test
Let’s look at a common example for evaluating and comparing classifiers for a balanced binary classification problem.
It is common practice to evaluate classification methods using classification accuracy, to evaluate each model using 10-fold cross-validation, to assume a Gaussian distribution for the sample of 10 model skill estimates, and to use the mean of the sample as a summary of the model’s skill.
We could require that each classifier evaluated using this procedure be evaluated on exactly the same splits of the dataset via 10-fold cross-validation. This would give samples of matched paired measures between two classifiers, matched because each classifier was evaluated on the same 10 test sets.
We could then select and use the paired Student’s t-test to check if the difference in the mean accuracy between the two models is statistically significant, e.g. reject the null hypothesis that assumes that the two samples have the same distribution.
In fact, this is a common way to compare classifiers with perhaps hundreds of published papers using this methodology.
The problem is, a key assumption of the paired Student’s t-test has been violated.
Namely, the observations in each sample are not independent. As part of the k-fold cross-validation procedure, a given observation will be used in the training dataset (k-1) times. This means that the estimated skill scores are dependent, not independent, and in turn that the calculation of the t-statistic in the test will be misleadingly wrong along with any interpretations of the statistic and p-value.
This observation requires a careful understanding of both the resampling method used, in this case k-fold cross-validation, and the expectations of the chosen hypothesis test, in this case the paired Student’s t-test. Without this background, the test appears appropriate, a result will be calculated and interpreted, and everything will look fine.
Unfortunately, selecting an appropriate statistical hypothesis test for model selection in applied machine learning is more challenging than it first appears. Fortunately, there is a growing body of research helping to point out the flaws of the naive approaches, and suggesting corrections and alternate methods.

### Summary of Some Findings
In this section, let’s take a look at some of the research into the selection of appropriate statistical significance tests for model selection in machine learning.

#### Use McNemar’s test or 5×2 Cross-Validation
Perhaps the seminal work on this topic is the 1998 paper titled “Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms” by Thomas Dietterich.
It’s an excellent paper on the topic and a recommended read. It covers first a great framework for thinking about the points during a machine learning project where a statistical hypothesis test may be required, discusses the expectation on common violations of statistical tests relevant to comparing classifier machine learning methods, and finishes with an empirical evaluation of methods to confirm the findings.
        `This article reviews five approximate statistical tests for determining whether one learning algorithm outperforms another on a particular learning task.`
The focus of the selection and empirical evaluation of statistical hypothesis tests in the paper is that calibration of Type I error or false positives. That is, selecting a test that minimizes the case of suggesting a significant difference when no such difference exists.
There are a number of important findings in this paper.
The first finding is that using paired Student’s t-test on the results of skill estimated via random resamples of a training dataset should never be done.
        `we can confidently conclude that the resampled t test should never be employed.`
The assumptions of the paired t-test are violated in the case of random resampling and in the case of k-fold cross-validation (as noted above). Nevertheless, in the case of k-fold cross-validation, the t-test will be optimistic, resulting in a higher Type I error, but only a modest Type II error. This means that this combination could be used in cases where avoiding Type II errors is more important than succumbing to a Type I error.
        `The 10-fold cross-validated t test has high type I error. However, it also has high power, and hence, it can be recommended in those cases where type II error (the failure to detect a real difference between algorithms) is more important.`
Dietterich recommends the McNemar’s statistical hypothesis test in cases where there is a limited amount of data and each algorithm can only be evaluated once.
McNemar’s test is like the Chi-Squared test, and in this case is used to determine whether the difference in observed proportions in the algorithm’s contingency table are significantly different from the expected proportions. This is a useful finding in the case of large deep learning neural networks that can take days or weeks to train.
        `Our experiments lead us to recommend […] McNemar’s test, for situations where the learning algorithms can be run only once.`
Dietterich also recommends a resampling method of his own devising called 5×2 cross-validation that involves 5 repeats of 2-fold cross-validation.
Two folds are chosen to ensure that each observation appears only in the train or test dataset for a single estimate of model skill. A paired Student’s t-test is used on the results, updated to better reflect the limited degrees of freedom given the dependence between the estimated skill scores.
        `Our experiments lead us to recommend […] 5 x 2cv t test, for situations in which the learning algorithms are efficient enough to run ten times`

#### Refinements on 5×2 Cross-Validation
The use of either McNemar’s test or 5×2 cross-validation has become a staple recommendation for much of the 20 years since the paper was published.
Nevertheless, further improvements have been made to better correct the paired Student’s t-test for the violation of the independence assumption from repeated k-fold cross-validation.
Two important papers among many include:
Claude Nadeau and Yoshua Bengio propose a further correction in their 2003 paper titled “Inference for the Generalization Error“. It’s a dense paper and not recommended for the faint of heart.
        `This analysis allowed us to construct two variance estimates that take into account both the variability due to the choice of the training sets and the choice of the test examples. One of the proposed estimators looks similar to the cv method (Dietterich, 1998) and is specifically designed to overestimate the variance to yield conservative inference.`
Remco Bouckaert and Eibe Frank in their 2004 paper titled “Evaluating the Replicability of Significance Tests for Comparing Learning Algorithms” take a different perspective and considers the ability to replicate results as more important than Type I or Type II errors.
        `In this paper we argue that the replicability of a test is also of importance. We say that a test has low replicability if its outcome strongly depends on the particular random partitioning of the data that is used to perform it`
Surprisingly, they recommend using either 100 runs of random resampling or 10×10-fold cross-validation with the Nadeau and Bengio correction to the paired Student-t test in order to achieve good replicability.
The latter approach is recommended in Ian Witten and Eibe Frank’s book and in their open-source data mining platform Weka, referring to the Nadeau and Bengio correction as the “corrected resampled t-test“.
        `Various modifications of the standard t-test have been proposed to circumvent this problem, all of them heuristic and lacking sound theoretical justification. One that appears to work well in practice is the corrected resampled t-test. […] The same modified statistic can be used with repeated cross-validation, which is just a special case of repeated holdout in which the individual test sets for one cross- validation do not overlap.`
— Page 159, Chapter 5, Credibility: Evaluating What’s Been Learned, Data Mining: Practical Machine Learning Tools and Techniques, Third Edition, 2011.

## Recommendations
There are no silver bullets when it comes to selecting a statistical significance test for model selection in applied machine learning.

Let’s look at five approaches that you may use on your machine learning project to compare classifiers.

### 1. Independent Data Samples
If you have near unlimited data, gather k separate train and test datasets to calculate 10 truly independent skill scores for each method.
You may then correctly apply the paired Student’s t-test. This is most unlikely as we are often working with small data samples.
        `the assumption that there is essentially unlimited data so that several independent datasets of the right size can be used. In practice there is usually only a single dataset of limited size. What can be done?`
— Page 158, Chapter 5, Credibility: Evaluating What’s Been Learned, Data Mining: Practical Machine Learning Tools and Techniques, Third Edition, 2011.

### 2. Accept the Problems of 10-fold CV
The naive 10-fold cross-validation can be used with an unmodified paired Student t-test can be used.
It has good repeatability relative to other methods and a modest type II error, but is known to have a high type I error.
        `The experiments also suggest caution in interpreting the results of the 10-fold cross-validated t test. This test has an elevated probability of type I error (as much as twice the target level), although it is not nearly as severe as the problem with the resampled t test.`
— Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms, 1998.
It’s an option, but it’s very weakly recommended.

### 3. Use McNemar’s Test or 5×2 CV
The two-decade long recommendations of McNemar’s test for single-run classification accuracy results and 5×2-fold cross-validation with a modified paired Student’s t-test in general stand.
Further, the Nadeau and Bengio further correction to the test statistic may be used with the 5×2-fold cross validation or 10×10-fold cross-validation as recommended by the developers of Weka.
A challenge in using the modified t-statistic is that there is no off-the-shelf implementation (e.g. in SciPy), requiring the use of third-party code and the risks that this entails. You may have to implement it yourself.
The availability and complexity of a chosen statistical method is an important consideration, said well by Gitte Vanwinckelen and Hendrik Blockeel in their 2012 paper titled “On Estimating Model Accuracy with Repeated Cross-Validation“:
        `While these methods are carefully designed, and are shown to improve upon previous methods in a number of ways, they suffer from the same risk as previous methods, namely that the more complex a method is, the higher the risk that researchers will use it incorrectly, or interpret the result incorrectly.`
I have an example of using McNemar’s test here: `How to Calculate McNemar’s Test to Compare Two Machine Learning Classifiers`

### 4. Use a Nonparametric Paired Test
We can use a nonparametric test that makes fewer assumptions, such as not assuming that the distribution of the skill scores is Gaussian.
One example is the Wilcoxon signed-rank test, which is the nonparametric version of the paired Student’s t-test. This test has less statistical power than the paired t-test, although more power when the expectations of the t-test are violated, such as independence.
This statistical hypothesis test is recommended for comparing algorithms different datasets by Janez Demsar in his 2006 paper “Statistical Comparisons of Classifiers over Multiple Data Sets“.
        `We therefore recommend using the Wilcoxon test, unless the t-test assumptions are met, either because we have many data sets or because we have reasons to believe that the measure of performance across data sets is distributed normally.`
Although the test is nonparametric, it still assumes that the observations within each sample are independent (e.g. iid), and using k-fold cross-validation would create dependent samples and violate this assumption.

### 5. Use Estimation Statistics Instead
Instead of statistical hypothesis tests, estimation statistics can be calculated, such as confidence intervals. These would suffer from similar problems where the assumption of independence is violated given the resampling methods by which the models are evaluated.
Tom Mitchell makes a similar recommendation in his 1997 book, suggesting to take the results of statistical hypothesis tests as heuristic estimates and seek confidence intervals around estimates of model skill:
        `To summarize, no single procedure for comparing learning methods based on limited data satisfies all the constraints we would like. It is wise to keep in mind that statistical models rarely fit perfectly the practical constraints in testing learning algorithms when available data is limited. Nevertheless, they do provide approximate confidence intervals that can be of great help in interpreting experimental comparisons of learning methods.`
— Page 150, Chapter 5, Evaluating Hypotheses, Machine Learning, 1997.
Statistical methods such as the bootstrap can be used to calculate defensible nonparametric confidence intervals that can be used to both present results and compare classifiers. This is a simple and effective approach that you can always fall back upon and that I recommend in general.
        `In fact confidence intervals have received the most theoretical study of any topic in the bootstrap area.`
— Page 321, An Introduction to the Bootstrap, 1994.
[ Source: `https://machinelearningmastery.com/statistical-significance-tests-for-comparing-machine-learning-algorithms/` ]