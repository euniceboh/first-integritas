<a name="readme-top"></a>

<!--https://www.markdownguide.org/basic-syntax/#reference-style-links-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/danielxdante/Project-First-Integritas">
    <img src="src/static/images/cpfLogo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">OAS Validator</h3>

<p align="center">
    Internal Web Application for OpenAPI Specification (YAML/JSON) Validator Tool
    <br />
    <a href="https://github.com/danielxdante/Project-First-Integritas"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/danielxdante/Project-First-Integritas">View Demo</a>
    ·
    <a href="https://github.com/danielxdante/Project-First-Integritas/issues">Report Bug</a>
    ·
    <a href="https://github.com/danielxdante/Project-First-Integritas/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![Product Home Screenshot][home-screenshot]

<p align="right">(<a href="#readme-top">Back to top</a>)</p>

### Built With

* ![[Flask][Flask.com]][Flask-url]
* ![[Express][Express.js]][Express-url]
* ![[Node][Node.js]][Node-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![Jest][Jest.js]][Jest-url]
* [![Selenium][Selenium.dev]][Selenium-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Sneak Peek

This repository contains a Dockerized application that provides YAML/JSON document validation according to the OpenAPI v3.0 specification and additional validation rules for CPF's API space.

### Prerequisites

Make sure you have the following prerequisites installed on your machine:

* Docker : [Installation Guide](https://docs.docker.com/engine/install/)
* Docker Compose (needed only if Docker V1 is installed on your machine): [Installation Guide](https://docs.docker.com/compose/install/linux/)

### Getting Started

Follow these steps to run the application using Docker:

1. Clone this repository to your local machine:

```
  git clone https://github.com/DanielxDante/Project-First-Integritas.git
```

2. Navigate to the project directory

```
  cd Project-First-Integritas
```

3. Build the Docker images using Docker Compose

```
  docker-compose up -d
```

4. Open your web browser and visit http://localhost/ to access the application
5. To stop the application, run:

```
  docker-compose down
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

* Input

To validate your YAML/JSON document, you can either type into the code editor on the left panel, or you can import your YAML/JSON file using the "Import File" button under "File".

* Validate

If your YAML/JSON document contains syntax errors, the code editor will automatically scroll and highlight the line where the syntax error occurred 

Once all syntax errors are resolved, wait for a few seconds for the result to appear on the right panel.

* Valid YAML/JSON Document

![Product Successful YAML/JSON Screenshot][success-screenshot]

An API preview of your YAML/JSON document will be displayed.

* Invalid YAML/JSON Document

![Product Unsuccessful YAML/JSON Screenshot][error-screenshot]

An accordion of errors will be displayed.

Additional information will be shown when the accordion items are clicked. The code editor will also automatically scroll and highlight the line where the error has occurred.

Specific rules that determine the errors can be found in the src/node/oas3.0_schema.yaml file.

* Save 

Once you are satisfied after editing your YAML/JSON on the code editor, you can save it using the "Save File" button under "File".

* Custom Dictionary

This YAML/JSON validator includes a spelling checking feature for titles, descriptions, and paths. To include custom words that you wish to include into the dictionary, add the words into the src/static/dictionary/customDictionary.txt file.

You can look at the words in your custom dictionary using the "View Dictionary" button in the web application.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Daniel Tay - danielonline170600@outlook.com

Project Link: [https://github.com/danielxdante/Project-First-Integritas](https://github.com/danielxdante/Project-First-Integritas)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Be the first!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/danielxdante/Project-First-Integritas.svg?style=for-the-badge
[contributors-url]: https://github.com/danielxdante/Project-First-Integritas/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/danielxdante/Project-First-Integritas.svg?style=for-the-badge
[forks-url]: https://github.com/danielxdante/Project-First-Integritas/network/members
[stars-shield]: https://img.shields.io/github/stars/danielxdante/Project-First-Integritas.svg?style=for-the-badge
[stars-url]: https://github.com/danielxdante/Project-First-Integritas/stargazers
[issues-shield]: https://img.shields.io/github/issues/danielxdante/Project-First-Integritas.svg?style=for-the-badge
[issues-url]: https://github.com/danielxdante/Project-First-Integritas/issues
[license-shield]: https://img.shields.io/github/license/danielxdante/Project-First-Integritas.svg?style=for-the-badge
[license-url]: https://github.com/DanielxDante/Project-First-Integritas/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/danieltaysg/
[home-screenshot]: src/static/images/Home.PNG
[success-screenshot]: src/static/images/Success.PNG
[error-screenshot]: src/static/images/Error.PNG
[JQuery-url]: https://jquery.com
[Jest.js]: https://img.shields.io/badge/Jest-v29.5.0-35495E?style=for-the-badge&logo=jest&logoColor=4FC08D
[Jest-url]: https://jestjs.io/
[Selenium.dev]: https://img.shields.io/badge/Selenium-v4.9.1-DD0031?style=for-the-badge&logo=selenium&logoColor=white
[Selenium-url]: https://www.selenium.dev/

[Flask.com]: https://img.shields.io/badge/Flask-v2.3.2-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/2.3.x/
[Express.js]: https://img.shields.io/badge/Express.js-v4.18.2-20232A?style=for-the-badge&logo=express&logoColor=61DAFB
[Express-url]: https://expressjs.com/
[Node.js]: https://img.shields.io/badge/Node.js-v18.12.1-35495E?style=for-the-badge&logo=node.js&logoColor=4FC08D
[Node-url]: https://nodejs.org/en
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-v5.2.0-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-v3.4.1-0769AD?style=for-the-badge&logo=jquery&logoColor=white
