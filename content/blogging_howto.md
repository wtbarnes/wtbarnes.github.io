Title: Blogging with Pelican, Jupyter, GitHub, and Travis CI
Date: 2016-03-31 1:21
Category: Pelican
Tags: pelican, blogging, jupyter, github, travis-ci
slug:blogging-howto
Authors: Will Barnes
Summary: A thorough walkthrough of how I setup this blog using Pelican so that I can write posts using Jupyter notebooks and publish it with GitHub Pages and Travis CI.

As a graduate student in physics, I wanted to maintain a personal webpage to advertise my current research projects to other researchers in my field and for the purpose of shamelessly self-promoting the few skills I've gained in graduate school in case I might one day want a real job.

I had previously built a single-page website that was hosted on my department's archaic SuSE Enterprise Linux server. This had a few downsides. To add content meant editing the raw HTML which often discouraged me from updating my page. Additionally, once I had made the desired changes on my local copy, I had to push the changes to GitHub and then ssh into the server and pull down the changes manually.

Pelican (and other static-site generators like [Jekyll](https://jekyllrb.com/)) solves this problem by letting you write all of your posts in Markdown and then auto-generating the HTML. I also found that [several other people had looked into writing blog posts with Jupyter notebooks](http://cyrille.rossant.net/pelican-github/) and had even [written Pelican plugins](http://danielfrg.com/blog/2013/02/16/blogging-pelican-ipython-notebook/) to make this process easier! This made Pelican a natural choice for someone already familiar with Python and who wants to write blog posts that may include a mixture of equations, code, figures, and (Markdown) text.

Below I've detailed how I setup this blog using Pelican so that I can write posts in both Markdown and Jupyter notebooks and then publish the site on GitHub Pages using Travis CI. I've made sure to link to the many blogs/docs that helped me so make sure to check out all of those links as well.

## GitHub Pages
Because we're going to host the blog on GitHub, we need to [set up a GitHub Pages repository](https://pages.github.com/). Basically this just involves creating a repository with the name `<username>.github.io` (where `<username>` is your GitHub username). Once you've created the repository, clone it and change into that directory:
```bash
$ git clone https://github.com/<username>.github.io.git
$ cd <username>.github.io
```
For a user site, GitHub will look for content on the `master` branch of the repo. Because we want to separate the files we'll be authoring and the actual content that will get served to the page, we'll create a new branch, call it `sources`, where we'll do all of our work. Create the branch and switch to it:
```bash
$ git branch sources
$ git checkout sources
```

## Pelican
[Pelican](http://blog.getpelican.com/) is a static site-generator written in Python. Think [Jekyll](https://jekyllrb.com/), but in Python instead of Ruby. Because we'll be working in Python, we can easily leverage the power of virtual environments via `conda`. You can also do this with `virtualenv`; most of the setup commands are roughly the same. (**Note:** If you aren't using [Anaconda](https://www.continuum.io/) to manage your Python installation, you're missing out.)

Let's setup an environment for our webpage and give it an original name, and activate it,
```bash
$ conda create --name webpage python=2.7
$ source activate webpage
```
Because we've isolated ourselves from the rest of our Python installation, we can easily manage all of the dependencies we need to get our blog up and running. First, let's install Pelican, Markdown and `ghp-import` (for force pushing content to `master`):
```bash
$ pip install pelican markdown ghp-import
```
Additionally, I found that I needed Jupyter and IPython in order to get the IPython notebooks plugin to work so let's go ahead and grab that too. (**Note:** Jupyter comes with a lot of dependencies so this may cause you're install to be a bit bloated. Some packages can probably be safely removed though I haven't looked into this):
```bash
$ pip install jupyter ipython
```
This should be all the dependencies we need so let's go ahead and save all of the required modules:
```bash
$ pip freeze > requirements.txt
```
This will make our Travis CI build much easier to configure.

It's finally time to build the site. To build the directory structure and create some of the needed files:
```bash
$ pelican-quickstart
```
Answer all of the questions according to how you want to setup your site. There will be a series of questions relating to how you want to publish your webpage. Answer `n` to all (`FTP`,`SSH`,`Dropbox`,`S3`,`Rackspace Cloud Files`) except `GitHub pages`. This will auto-generate a Makefile option to make publishing easy. The resulting directory tree should look something like this:
```
├── Makefile
├── content/          #put your content here
├── develop_server.sh
├── fabfile.py
├── output/           #auto-generated content will go here
├── pelicanconf.py
└── publishconf.py
```
The `pelicanconf.py` file defines all of the configuration for your site and has been pre-populated with the answers you supplied during the quickstart.

Pelican assumes any `.md` file inside of `content/` is a blog entry and will treat it as such. See [here](http://docs.getpelican.com/en/stable/content.html) for more info on authoring content. Put any non-blog pages (e.g. "About", "Contact", "CV", etc.) in a subdirectory `content/pages/`. Pelican will treat these as [non-chronological](http://docs.getpelican.com/en/stable/content.html#pages) rather than just listing them in the blogroll.

## Testing Locally
Time to make some content and see if this worked! Write a test blog post and put it in `content/` and a test About-me page and put it in `content/pages/`:

### `content/my_first_blog.md`
```markdown
Title: Blogging with Pelican, Jupyter, GitHub, and Travis CI
Date: 2016-04-02 18:05
Category: Pelican
Tags: pelican, blogging, test
slug:a_test
Authors: Foo Bar
Summary: A test blog entry

This is my first blog entry and it is a test.
```
### `content/pages/about.md`
```markdown
---
Title: About
---

This is the about me page. Here are some things about me.
```
Now that we've written some content, we need to generate the raw HTML. The Makefile generated by `pelican-quickstart` gives us an option for doing this:
```bash
$ make html
```
If you take a look in `output/`, you'll see all of your content there. However, for testing your site locally, it'd be nice to have these served and updated automatically. Again, the makefile provides us this option:
```bash
$ make devserver
```
If you navigate to `localhost:8000`, you should see your page. As you make changes (e.g. add posts and pages, change themes, etc.), you should see these reflected your served HTML. To stop the server:
```bash
$ make stopserver
```

## Installing themes
To customize the look of your webpage, Pelican provides the `THEME` variable in `pelicanconf.py`. [There are many different Pelican themes](http://www.pelicanthemes.com/) and an official repository is maintained [here](https://github.com/getpelican/pelican-themes). This website uses the [pelican-bootstrap3 theme](https://github.com/DandyDev/pelican-bootstrap3). To install a theme, first create a directory to store them (you may want to switch between a few):
```bash
$ mkdir themes/
```
You can either just copy the directory containing the theme you want into here or add the theme repository as a submodule. I've opted for the latter so that I can incorporate any updates to the theme:
```bash
$ cd themes/
$ git submodule add https://github.com/<theme_user>/<theme_repo>.git
```
Pelican also includes [a tool for installing and managing your themes](http://docs.getpelican.com/en/stable/pelican-themes.html). Once you have the theme installed, set the `THEME` variable in `pelicanconf.py` appropriately:
```python
THEME='themes/<my_installed_theme>'
```

## Writing posts with Jupyter notebooks
To use Jupyter notebooks as posts, we'll use [plugins](http://docs.getpelican.com/en/stable/plugins.html), a way to easily extend the functionality of your Pelican webpage. An official repository of plugins is maintained [here](https://github.com/getpelican/pelican-plugins). We'll be using the [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb) which at the time of this writing has not yet been incorporated into the official plugin repository.

Following [this approach by Cyrille Rossant](http://cyrille.rossant.net/pelican-github/), we're going to have a directory for custom plugins(i.e. not in the official repo), `plugins/`, and a directory with all of the official plugins, `pelican-plugins`. The latter can be added as a submodule. You can off course pick-and-choose which plugins you want and just copy and paste those into a single directory if you want.
```bash
$ mkdir plugins
$ git submodule add https://github.com/getpelican/pelican-plugins.git
```
We need to tell Pelican where to look for these plugins and which ones we'll be using. pelican-ipynb depends on [Jake Vanderplas's liquid_tags plugin](https://github.com/getpelican/pelican-plugins/tree/master/liquid_tags) (included in `pelican-plugins`) so we'll need to point to that one too. In `pelicanconf.py`:
```python
PLUGIN_PATHS=['pelican-plugins','plugins']
PLUGINS=['liquid_tags.notebook','ipynb.liquid',]
```

Follwing the [pelican-ipynb installation guide](https://github.com/danielfrg/pelican-ipynb), I've opted for "Mode B: Liquid Tags". This will essentially allow us to inject notebook content straight into a normal `.md` file. First, create a directory to store the notebooks,
```bash
$ mkdir content/notebooks
```
and add a notebook to this new directory (e.g. `contents/notebooks/my_test_notebook.ipynb`). Then tell Pelican to preserve the path to this directory so that we can pull content from it. In `pelicanconf.py`:
```python
STATIC=['notebooks']
```
Finally, we can add this as a blog entry by injecting into a normal Markdown blog entry, `contents/hello_jupyter.md`:
```
Title: Hello Pelican with Jupyter!
Date: 2016-04-03 0:54
Category: Pelican
Tags: pelican, python, jupyter
slug:hello-jupyter
Authors: Foo Bar
Summary: This blog post was written in a Jupyter notebook. It can be included in a post using a liquid tag.

{% notebook notebooks/my_test_notebook.ipynb %}
```
This post should now be available on your main blog roll and the content should all be rendered from your Jupyter notebook, figures, LaTeX, Markdown, and all!

## Automatic Builds with Travis CI
Now we want to publish our site with GitHub Pages. By default, any content on the `master` branch of your repo will be available at `<username>.github.io`. Every time we edit our content on the `sources` branch and push it to GitHub, we would like these changes to be reflected on our actual site.
A continuous integration service like [Travis CI](https://travis-ci.org/) allows you to leverage GitHub's web hooks to trigger builds of your website at each commit to `sources`.

Login to Travis CI with your GitHub username and enable your `<username>.github.io` repository. Then we need to provide a `.travis.yml` configuration file to tell Travis what to do at each commit. The `.travis.yml` for this blog looks like:
```travis
language: python
python:
- '2.7'
sudo: required
branches:
  only:
  - sources
install:
- pip install -r requirements.txt
script:
- make publish github
env:
  global:
    secure: xxxxxxxxx
```
This tells Travis that we're using Python, version 2.7, that we only want to trigger builds when pushing to the `sources` branch, to install every package in our `requirements.txt` file, and to run the `make` with the `publish github` option. This will use `ghp-import` to put a copy of everything in `output/` on `master` and then do a force push to `master`

This last line contains a key that will allow Travis to do a force push to the `master` branch. Generate using [the instructions listed here](http://blog.mathieu-leplatre.info/publish-your-pelican-blog-on-github-pages-via-travis-ci.html). Finally, in order to give Travis all the permissions it needs for the force push, replace the second line in the `github: publish` block of `Makefile` with:
```bash
git push -f https://${GH_TOKEN}@github.com/${TRAVIS_REPO_SLUG} $(GITHUB_PAGES_BRANCH)
```

That's pretty much it. Author some posts, add a theme and push to the `sources` branch and Travis and GitHub should take care of the rest. You can see any errors that get thrown by going to your Travis CI homepage. For a complete working example, [check out the source for this site on my GitHub page.](https://github.com/wtbarnes/wtbarnes.github.io/tree/sources)

## Other Great Resources

Without the plethora of blogs and tutorials on Pelican, GitHub, and Travis that already exist, setting up this blog would have been **much** more difficult (read _impossible_). Here are some resources that I found really helpful while putting this all together:

* [Setting up a blog with Pelican and GitHub Pages, Cyrille Rossant](http://cyrille.rossant.net/pelican-github/)
* [GitHub Pages](https://pages.github.com/)
* [Publish your Pelican blog on Github pages via Travis-CI, Mathieu Leplatre](http://blog.mathieu-leplatre.info/publish-your-pelican-blog-on-github-pages-via-travis-ci.html)
* [Pelican Docs](http://docs.getpelican.com/en/3.6.3/)
* [Many examples of Pelican Themes](http://www.pelicanthemes.com/)
* [Blogging with IPython notebooks in pelican, Daniel Rodriguez](http://danielfrg.com/blog/2013/02/16/blogging-pelican-ipython-notebook/)
