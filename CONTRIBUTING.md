# Contributing to EarthWorks

Thanks for taking the time to contribute!

This guide is a work in progress. For now the best place to start is the [Issues](https://github.com/EarthWorksOrg/EarthWorks/issues) for a problem or feature request, the [Pull Requests](https://github.com/EarthWorksOrg/EarthWorks/pulls) to add your own changes, or [Discussions](https://github.com/EarthWorksOrg/EarthWorks/discussions) for all other topics. Please search before posting to keep the duplicates low! 

## Code of Conduct

The EarthWorks project and all participants are governed by our [Code of Conduct](https://github.com/EarthWorksOrg/EarthWorks/blob/main/CODE_OF_CONDUCT.md). Upholding this code and reporting any violations to <need_email_here> ensures the quality of our community. Thank you for the efforts to keep this an open and welcoming environment!

## Before Starting

### EarthWorks Repositories and Externals
<!--- Expand this section to explain that the main repo contains (some meta files) an Externals.cfg and a utility to process it to fetch the "Externals"  --->
The EarthWorks Model (this repo) initially contains a few "meta" files about the repository (this Contributors' Guide, the LICENSE, etc), a cime_config folder, a folder containing the `manage_externals` tool, and the Externals.cfg file. Once a user runs the `./manage_externals/checkout_externals` command, the rest of the model source code will be fetched from the [Externals]() according to the contents of Externals.cfg. This will create and populate (sub)directories including `ccs_config`, `cime`, `components`, `libraries`, `share`, and `tools`.

### Some Important Terms
<!--- Add definitions and explanations for select important terms --->
#### External
An **external** is any source code or repository that is used by EarthWorks and isn't contained in the main model repository ([EarthWorksOrg/EarthWorks](https://github.com/EarthWorksOrg/EarthWorks)). These are defined in the Externals.cfg.

#### EarthWorks External (EW External)
An **EarthWorks external** is an external that uses an EarthWorksOrg fork instead of the usual upstream repository. For example EarthWorks uses the EarthWorksOrg/CAM repository instead of the ESCOMP/CAM repository. These forks have been created to allow the EarthWorks team to add their own changes that may not be suitable for general CESM or other upstream development. We try to keep this forks reasonably up-to-date with upstream development. Some other conventions about EarthWorks externals include: 

- The two most important branches are the `ew-main` and `ew-develop` branches which behave as the `main` and `develop` branches in other repositories.
- All tags in external repos are "annotated" so that the last line describes what the upstream repo is and what tag was last synchronized from the upstream. E.g. the tag cam-ew2.1.000:
  > Start new dev cycle after EarthWorks 2.1 release
	>
	> Last changes from upstream 'ESCOMP/CAM' tag:'cam6_3_145
- Issues, Discussions, and Feature Requests should originate in the EarthWorksOrg/EarthWorks repo to ease the points of communication. If you have any confusion, please try to reach out to us at <need_email_here>
  - Pull Requests are different, these should always begin in whichever repository or codebase they apply to.

## How Can I Contribute?
<!--- Once they know what they should, how can they interact? --->
Generally the best way to get involved is to check the [Issues Page](), either to submit your own issue or to get involved with those already posted! Some ways to get involved include:
- [Report a Problem or Bug]()
- [Suggest or Request Enhancements]()
- Add your own changes ([Pull Requests]())
- Extend the documentation in the EarthWorks README or [Wiki]() 

**Please search before posting**, there may already be another thread about your topic. We will redirect conversation and close duplicates in efforts to keep communication clear.

Also please try to stay involved! Any Issue or Pull Request that is inactive and deemed irrelevant by the EarthWorks team will be closed.

### Report a Problem or Bug
<!--- Where should reports go? Anything they should do before or to make sure they have a "good" submission? --->
**Important:** if you think you have found a security vulnerability do NOT open an Issue or make a public post. Instead email <need_email_here>.

If you notice unexpected model behavior, build failures, poor outputs, or many other problems please head over to the Issues Page.

A good issue starts with a short and descriptive title, typically less than 72 characters. The body of the issue should expand on the title to describe the issue and provide specifics. A good body typically answers the questions:

- What steps were taken to produce the problem?
- What did you expect to happen? What occured instead?
- What was:
  - the machine (computer) you were working on?
	- tag or version of EarthWorks you were using? Did you make any modifications?
	- what software stack (especially compiler) were you using?
- What was the exact text of any error message in your build or run logs? (Please copy/paste what seems relevant)
- If on a NSF NCAR system, is there a path to a relevant case you think would help?

### Suggest or Request Enhancements
<!--- What should be done so a request is easy to understand and likely to see prompt engagement (triage, wontfix, or discussion towards implementation) --->
If there is something you wish EarthWorks had or a change you would like to see, please go to the Issues page. If you searched and didn't find a similar enough post you can create a new Issue with your feature request. Please take some time to describe:

- What change you would like to see.
- Why you need this change (and any impact).
- How you think the change should work.
- If and where the change already exists. (I.e. do you have a branch with these changes already?)
- What existing tests exercise this change or must be added.

Someone from the EarthWorks team will try to take a look at your suggestions to decide if the change is a duplicate, is something that won't be fixed, is something that can be implemented easily, or is something that needs further discussion. 

### Pull Requests
<!--- What should, needs, or must be done for maintainers to consider your changes --->
Pull Requests (PRs) are the main way that changes and fixes are applied to EarthWorks and the externals. PRs allow for discussion around changes before they are formally accepted and merged into the base branch of the PR. For general information about a PR, please consult the GitHub documentation: [About pull requests](). If you haven't made a PR before, please consider making a [Feature Request]() in the Issues Page first to better collaborate with the EarthWorks team.

### Documentation or Guides

### Share Your Results!

## Styleguides and Requirements

## Additional Notes

### Repository Conventions

#### Tagging

#### GitHub Labels

#### Important Terms

