# PharmaTowi

## Quick Overview
This website was designed as the final project for the Web technologies course of 2018-2019.
The goal of this website was to provide a platform for consumers to be able to order the required medicines through an online portal. For pharmacists, this website was aimed to simplify the workflow as well as offer simplified exposure.

## Functionality
- Registration and login system for new users and pharmacists.
- Phone registration (using the free Twilio API)
- Basic user profile as well as being able to edit this profile
- Change password functionality
- Pharmacists are able to start a pharmacy on the website
- Pharmacists can add stock to their pharmacy
- Order online out of the available stock of a pharmacist
- Pharmacists are able to fill this order, after which the user gets a notification through their email
- Users are able to rate a pharmacy as well as leave comments on the page about their experience with this pharmacy
- Look up pharmacies via a search query as well as via a visual map (using the Mapbox API)

## Technologies Used
In order to provide the different functionalities we had to employ a range of technologies. For a full set of requirements, please see the requirements.txt file in the root of the project.

- Django: The platform was developed using the Django framework
- HTML(5)
- CSS: The bootstrap framework was used. This allowed us to provide a good mobile experience as well as desktop.
- Javascript
- Ajax: Ajax was used multiple times throughout this platform. For example in generating the map with the pharmacies and when rating and posting comments. This allows us to display new content without the user having to reload the page.
- Mapbox and Twilio API

## Contributors
Maxime Antoine
Thomas Vaeyens
Willem Röpke
