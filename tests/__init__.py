'''
testing is kind of despair. Here's what I need to focus on:

1. test individual algorithms thoroughly to make sure they work as intended
2. test specific functions (like Rosenbrock) under specific conditions and compare to scipy (time and quality)
3. DO NOT try to do specific tests in full generality because it will never work. For each function do a few tests from
        different starting points and end conditions, which are determined on a test by test basis

- start points are okay in function objects so long as we don't parametrize the functions themselves
- end conditions are a case by case thing so make a template kind of thing to make it easier to write but can't pair
        it with the function because different methods converge at different rates
'''