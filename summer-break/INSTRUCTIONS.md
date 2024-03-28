# Overview

This exercise will provide us with a working piece of code that can serve as neutral ground for technical discussion and as an element in candidate evaluation. 

We expect the excercise to take 2-3 hours and recommend that you do not spend any more than that, regardless of completion. Please read this entire document before beginning.

Feel free to use whatever resources you need. Just like in the real world, Google, Stackoverflow, etc. are tools of the trade. However, please make the work your own (don't copy from other solutions or ask for outside help).

We prefer Python, but will accept solutions in other languages.


# The Problem - Summer Break

You are contacted by a friend in desperate need of help - they have just spent the summer mowing lawns and, while they made good money, they forgot that they need to declare their income and expenses for tax purposes! You have been asked to use your programming prowess to help them out. The good news is that they kept all their invoices and receipts and have already performed the data-entry task. They merely need you to process the data and yield a tax-friendly report. You ask them why they don't just use [a spreadsheet, Turbo Tax, etc] but they scoff at your lack of DIY enthusiasm, alas.

Indulging your friend, you agree to develop a web service API that allows submission of data files and the ability to query the resulting aggregate data for the summer.

Their data entry exercise has resulted in a file tracking revenue and expenses, formatted as follows:

`Date, Type, Amount($), Memo`

Where `Type` is one of "Income" or "Expense" and `Memo` is either an expense category or job address (both just strings)

For example:
```
2020-07-01, Expense, 18.77, Gas
2020-07-04, Income, 40.00, 347 Woodrow
2020-07-06, Income, 35.00, 219 Pleasant
2020-07-12, Expense, 49.50, Repairs
```

Your web service must have the following API endpoints:

`POST /transactions`

Take as input the CSV formatted data as above, parse, and store the data.

`GET /report`

Return a JSON document with the tally of gross revenue, expenses, and net revenue (gross - expenses) as follows:

```
{
    "gross-revenue": <amount>,
    "expenses": <amount>,
    "net-revenue": <amount>
}
```

# Your solution

Prepare code to solve the problem. We encourage you to be mindful of time and start with an MVP solution and iterate if time permits (hint: you may not need persistence in your MVP).

Include a README with at least the following:

- Instructions for environment setup and running your code and tests
- Any additional context on your solution and approach, including any assumptions made
- What are the shortcomings of your solution?
- If you had additional time to work on this problem, what would you add or refine?

# Submitting results

Create a tarball of your solution **with your full name as part of the filename** and submit via the Greenhouse link that was provided via email.

If you have any questions please reply via email and we will do our best to help out.

Good luck!
