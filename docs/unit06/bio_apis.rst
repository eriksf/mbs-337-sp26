iNaturalist, RCSB, and NCBI
===========================

In this section, we will explore three popular APIs in the field of bioinformatics: `iNaturalist <https://www.inaturalist.org/>`_,
`RCSB Protein Data Bank <https://www.rcsb.org/>`_ (Research Collaboratory for Structural Bioinformatics), and
`NCBI <https://www.ncbi.nlm.nih.gov/>`_ (National Center for Biotechnology Information). These APIs provide
access to a wealth of biological data, including species observations, protein structures, and genomic
information. After going through this module, students should be able to:

- Understand the purpose and functionality of each API.
- Make API requests to retrieve data from each platform.
- Parse and utilize the retrieved data for various applications in bioinformatics.

iNaturalist
-----------

iNaturalist is a citizen science project and online social network of naturalists, citizen scientists,
and biologists built on the concept of mapping and sharing observations of biodiversity across the globe.
The hundreds of thousands of members share close to one million observations of plants, animals, fungi,
and other organisms every month. The iNaturalist API allows users to access data about species observations,
including information about the location, date, and species observed.


.. figure:: images/iNaturalist.png
    :width: 600px
    :align: center

    iNaturalist main site.

Let's take a look at the iNaturalist API documentation to understand how to make requests and retrieve data.


.. figure:: images/iNaturalist_api.png
    :width: 600px
    :align: center

    iNaturalist API documentation.

As the iNaturalist API documentation shows, we can make requests to retrieve observations. Since it is a
standard RESTful API, we could use the ``requests`` library in Python to interact with it. But there is an
easier way to interact with the iNaturalist API using the ``pyinaturalist`` library, which provides a more
user-friendly interface for accessing the API. So let's install the ``pyinaturalist`` library.

.. code-block:: console

   [mbs337-vm]$ cd $HOME/mbs-337
   [mbs337-vm]$ source .venv/bin/activate
   (.venv) [mbs337-vm]$ pip3 install pyinaturalist
   (.venv) [mbs337-vm]$ pip3 list
   Package              Version
   -------------------- -----------
   annotated-types      0.7.0
   attrs                25.4.0
   biopython            1.86
   cattrs               26.1.0
   certifi              2026.1.4
   cffi                 2.0.0
   charset-normalizer   3.4.4
   cryptography         46.0.5
   idna                 3.11
   iniconfig            2.3.0
   jaraco.classes       3.4.0
   jaraco.context       6.1.0
   jaraco.functools     4.4.0
   jeepney              0.9.0
   keyring              25.7.0
   markdown-it-py       4.0.0
   mdurl                0.1.2
   more-itertools       10.8.0
   numpy                2.4.1
   packaging            26.0
   pip                  24.0
   platformdirs         4.9.2
   pluggy               1.6.0
   pycparser            3.0
   pydantic             2.12.5
   pydantic_core        2.41.5
   Pygments             2.19.2
   pyinaturalist        0.21.1
   pyrate-limiter       2.10.0
   pytest               9.0.2
   python-dateutil      2.9.0.post0
   redis                7.2.0
   requests             2.32.5
   requests-cache       1.3.0
   requests-ratelimiter 0.8.0
   rich                 14.3.3
   SecretStorage        3.5.0
   six                  1.17.0
   typing_extensions    4.15.0
   typing-inspection    0.4.2
   url-normalize        2.2.1
   urllib3              2.6.3

Now that we have the ``pyinaturalist`` library installed, we can start making requests to the iNaturalist API.
Before we dive into the code, let's take a moment to look at the `API documentation <https://pyinaturalist.readthedocs.io/en/stable/reference.html>`_
for the ``pyinaturalist`` library to understand how to use it effectively.


.. figure:: images/iNaturalist_api_docs_get_observations.png
    :width: 600px
    :align: center

    iNaturalist API reference for `get_observations`.

OK, let's try to retrieve some observations for a 1 km radius around the coordinates (30.2895, -97.7368) which
is the location of the University of Texas at Austin for a 1 week period. We can use the following code to do
this:

.. code-block:: console

   [mbs337-vm]$ python3
   Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import pyinaturalist as pin
   >>> from rich import print
   >>>
   >>> obs = pin.get_observations(lat="30.2895", lng="-97.7368", radius=1, d1="2026-02-18", d2="2026-02-24")
   >>> pin.pprint(obs)

     ID          Taxon ID   Taxon                                  Observed on    User              Location
    -------------------------------------------------------------------------------------------------------------------------------------
     339941488   18205      Melanerpes carolinus (Red-Bellied      Feb 23, 2026   johnathan12034    W 30th St, Austin, TX, US
                            Woodpecker)
     339919433   1427972    Irpex latemarginatus (Frothy           Feb 23, 2026   kirsten24         701 Dean Keeton/San Jacinto, Austin,
                            Porecrust)                                                              TX 78705, USA
     339917918   81708      Aesculus pavia (Red Buckeye)           Feb 23, 2026   kirsten24         Travis County, US-TX, US
     339841781   118492     Helicoverpa zea (Corn Earworm Moth)    Feb 22, 2026   kuramazilla       Speedway, Austin, TX, US
     339835262   43111      Sylvilagus floridanus (Eastern         Feb 21, 2026   lauren1414        W 24th St, Austin, TX, US
                            Cottontail)
     339813315   164229     Jasminum mesnyi (Primrose Jasmine)     Feb 19, 2026   rebraph           San Jacinto Blvd, Austin, TX, US
     339806172   47126      Kingdom Plantae (Plants)               Feb 22, 2026   bradc559          San Antonio St, Austin, TX, US
     339726755   54900      Papilio polyxenes asterius (Eastern    Feb 21, 2026   utfarmstand       The University of Texas at Austin,
                            Black Swallowtail)                                                      Austin, TX, US
     339668489   164038     Ilex cornuta (Chinese Holly)           Feb 21, 2026   liljegrenv        Rio Grande St, Austin, TX, US
     339657223   4956       Ardea herodias (Great Blue Heron)      Feb 21, 2026   vivian38785       San Jacinto Blvd, Austin, TX, US
     339645270   8229       Cyanocitta cristata (Blue Jay)         Feb 21, 2026   chasek29          701 Dean Keeton/San Jacinto, Austin,
                                                                                                    TX 78705, USA
     339645214   13858      Passer domesticus (House Sparrow)      Feb 21, 2026   vivian38785       Rio Grande St, Austin, TX, US
     339642368   48502      Cercis canadensis (Eastern Redbud)     Feb 21, 2026   chasek29          701 Dean Keeton/San Jacinto, Austin,
                                                                                                    TX 78705, USA
     339642071   47351      Genus Prunus (Plums, Cherries, And     Feb 21, 2026   chasek29          701 Dean Keeton/San Jacinto, Austin,
                            Allies)                                                                 TX 78705, USA
     339573515   9607       Quiscalus mexicanus (Great-Tailed      Feb 21, 2026   avi_subramanian   Austin
                            Grackle)
     339501990   41663      Procyon lotor (Common Raccoon)         Feb 20, 2026   kuramazilla       E 24th St, Austin, TX, US
     339495572   14886      Mimus polyglottos (Northern            Feb 18, 2026   mariaks16         W 24th St, Austin, TX, US
                            Mockingbird)
     339488649   57056      Medicago lupulina (Black Medick)       Feb 20, 2026   adrianj           Red River St, Austin, TX, US
     339365066   103498     Ischnura posita (Fragile Forktail)     Feb 19, 2026   etaan             Cedar St, Austin, TX, US
     339331168   47124      Class Magnoliopsida (Dicots)           Feb 19, 2026   lexi_moffett      The University of Texas at Austin,
                                                                                                    Austin, TX, US
     339202074                                                     Feb 18, 2026   chrismyzoo        Austin
     339197531   1555999    Nephroia carolina (Carolina            Feb 18, 2026   utfarmstand       E 21st St, Austin, TX, US
                            Snailseed)

   >>>

Another nice thing we can do with the ``pyinaturalist`` library is to use their data models. This allows us to
work with the data in a more structured way as opposed to working with raw dictionaries. For example, we can use
the ``Observation`` data model to access observation attributes more easily and take a look at one observation.

.. code-block:: console

   >>> my_obs = pin.Observation.from_json_list(obs)
   >>> type(my_obs[14])
   <class 'pyinaturalist.models.observation.Observation'>
   >>> print(my_obs[14])
   Observation(
    id=339573515,
    created_at='2026-02-21 09:11:43-06:00',
    captive=False,
    community_taxon_id=9607,
    identifications_count=3,
    identifications_most_agree=True,
    identifications_most_disagree=False,
    identifications_some_agree=True,
    location=(30.2868747711, -97.7400512695),
    mappable=True,
    num_identification_agreements=3,
    num_identification_disagreements=0,
    oauth_application_id=333,
    obscured=False,
    observed_on='2026-02-21 09:11:37-06:00',
    owners_identification_from_vision=True,
    place_guess='Austin',
    place_ids=[
        1,
        18,
        431,
        9853,
        53217,
        53218,
        53222,
        59613,
        60211,
        62332,
        63856,
        64422,
        64423,
        65181,
        66741,
        67465,
        68119,
        80998,
        82256,
        97394,
        113590,
        124748,
        146145,
        148549,
        151222,
        151232,
        160119
    ],
    positional_accuracy=15,
    preferences={'prefers_community_taxon': None},
    public_positional_accuracy=15,
    quality_grade='research',
    reviewed_by=[115129, 3953595, 4483440, 8880881],
    site_id=1,
    species_guess='Great-tailed Grackle',
    taxon_geoprivacy='open',
    updated_at='2026-02-21 14:06:02-06:00',
    uri='https://www.inaturalist.org/observations/339573515',
    uuid='26673574-3cd1-470c-a6b9-ad36b4d8a580',
    annotations=[],
    application=None,
    comments=[],
    faves=[],
    flags=[],
    identifications=[
        Identification(
            id=765249631,
            username='isaaceastland',
            taxon_name='Quiscalus mexicanus (Great-Tailed Grackle)',
            created_at='Feb 21, 2026',
            truncated_body=''
        ),
        Identification(
            id=765180592,
            username='avi_subramanian',
            taxon_name='Quiscalus mexicanus (Great-Tailed Grackle)',
            created_at='Feb 21, 2026',
            truncated_body=''
        ),
        Identification(
            id=765182296,
            username='bobthebob101',
            taxon_name='Quiscalus mexicanus (Great-Tailed Grackle)',
            created_at='Feb 21, 2026',
            truncated_body=''
        ),
        Identification(
            id=765289717,
            username='aguilita',
            taxon_name='Quiscalus mexicanus (Great-Tailed Grackle)',
            created_at='Feb 21, 2026',
            truncated_body=''
        )
    ],
    ofvs=[],
    photos=[Photo(id=617763422, url='https://static.inaturalist.org/photos/617763422/square.jpg')],
    project_observations=[],
    quality_metrics=[],
    sounds=[],
    taxon=Taxon(id=9607, full_name='Quiscalus mexicanus (Great-Tailed Grackle)'),
    user=User(id=4483440, login='avi_subramanian', name='Avi Subramanian'),
    votes=[]
 )

Since we are using the data model, we can easily access the attributes of the observation.
For example, we can access the taxon name.

.. code-block:: console

 >>> print(my_obs[14].taxon.full_name)
 Quiscalus mexicanus (Great-Tailed Grackle)

And we can also access the photos associated with the observation.

.. code-block:: console

 >>> print(my_obs[14].photos)
 [
    Photo(
        id=617763422,
        attribution='(c) Avi Subramanian, all rights reserved',
        original_dimensions=(1152, 2048),
        url='https://static.inaturalist.org/photos/617763422/square.jpg'
    )
 ]

.. figure:: images/observation_photo_grackle_medium.jpg
    :align: center

    Photo of the Great-Tailed Grackle observation.


RCSB Protein Data Bank
----------------------
