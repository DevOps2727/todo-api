# To-Do List API

A small REST API for managing a to-do list, built with Python and Flask, containerised with Docker, and built automatically on every push via GitHub Actions.

Tasks are stored in memory, so they are cleared whenever the application restarts.

---

## Running it

### With Docker (recommended)

>>bash
docker build -t todo-api .
docker run -p 5000:5000 todo-api

The API is then available at `http://localhost:5000`.

### Locally with Python

>>bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py


---

## Endpoints

| POST | Add a new task |
| GET  | List all tasks |
| PATCH  | Mark a task as done |
| GET |  Health check |




## Notes on the Dockerfile

**python:3.13-slim as the base.** 
The full `python:3.13` image is roughly 1GB the slim variant is around 130MB.
That means faster pulls in CI, faster deploys.


**Dependencies are copied and installed before the application code.**
Docker caches each instruction as a layer and reuses the cache when the inputs have not changed. 
Because "requirements.txt' is copied and installed first, editing "app.py" does not invalidate the install layer, 
so rebuilds skip reinstalling Flask. Copying everything in one step would force a full reinstall on every code change.

**CMD uses exec form.** 
CMD ["python", "app.py"]` runs Python directly. 


**Versions are pinned.** 
Both the base image and the Python dependencies are pinned to specific versions,
so a rebuild months from now produces the same image rather than silently picking up a new major release.

---

## Continuous integration

.github/workflows/build.yml" runs on every push and pull request to "main". 
It checks out the repository on a clean Ubuntu runner and builds the Docker image.

The value is that the runner has none of my local setup — no virtual environment, no Docker Desktop, not even Windows. 
If the build passes there, the Dockerfile genuinely works from a fresh checkout rather than depending on something I happen to have installed.

---

## Reflection

>>> Trickiest part

The part that took me longest had nothing to do with the code. When I pushed from my terminal, the commits appeared under a different GitHub account than the one that owned the repository, and the workflow file I created through the GitHub web editor was attributed to the correct account. The result was a repository that looked like two different people had worked on it.

It took me a while to work out why, because nothing was broken — the push succeeded and the build passed. The cause was that my local `git config` email was tied to a different GitHub account. Git identity and GitHub account are separate things, and GitHub matches commits to profiles by the email address in the commit. Once I understood that, the fix was to set the correct email locally, amend the commit with `--reset-author`, and force-push.

This was the first time I had run into that problem, and it stuck with me more than the Docker work did, because the symptom gave no hint about the cause.

### Why I made these choices

>>>The base image choice is the one I would defend most readily. `python:3.13-slim` gives a much smaller image than the full variant, which means faster CI builds, faster deployments, and a smaller set of installed packages to worry about from a security perspective. For an application that only needs Flask, the extra tooling in the full image is dead weight.

I also deliberately split the copy steps in the Dockerfile so that dependency installation is cached separately from the application code, which makes rebuilds significantly faster during development.

### If I had another day

>>>I would take the pipeline one step further and actually deploy it. 
The workflow would push the built image to Amazon ECR, and a server would pull that image and run it. 
Registry credentials would come from GitHub secrets rather than being written into the workflow file.

