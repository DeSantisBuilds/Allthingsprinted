# Photography shot list

Real photos of All Things Printed work are the biggest remaining gap (see the audit). Each photo below has a slot ready on the site. Until a real photo is added, the slot is shown only in the private development preview, labelled *ESPACE PHOTO TEMPORAIRE / TEMPORARY PHOTO SLOT*, and never on the public site.

**Only use photos of real work by All Things Printed.** Do not use supplier catalogue images, AI-generated images or other shops’ work as “our work”. Ask customers before showing their logo or their people.

## How to shoot

- Daylight or bright, even light; no harsh flash. A plain wall or table behind the item.
- Landscape, 4:3 ratio (the site crops to 4:3), at least 1600 × 1200 px. Phone photos are fine.
- One clear subject per photo; fill the frame. Clean, flat, lint-free garments.
- For each photo, note: service, product, a short French and English caption, and whether the customer agreed to it being shown.

## Home page (6 photos)

- [ ] Commande de t-shirts d’entreprise / Corporate T-shirt order
- [ ] Vitrine lettrée / Lettered storefront
- [ ] Polos brodés / Embroidered polos
- [ ] Kangourous d’équipe / Team hoodies
- [ ] Monogramme de mariage / Wedding monogram
- [ ] Articles promotionnels / Promotional items

## Vêtements personnalisés / Custom apparel (3 photos)

- [ ] Pile de t-shirts imprimés, logo bien visible / Stack of printed T-shirts, logo clearly visible
- [ ] Employé portant un polo brodé (de face) / Employee wearing an embroidered polo (front)
- [ ] Détail rapproché d’une impression DTF / Close-up of a DTF print

## Impression DTF / DTF printing (3 photos)

- [ ] Design multicolore imprimé en DTF sur un t-shirt foncé / Multicolour DTF design on a dark T-shirt
- [ ] Détail rapproché des couleurs et du dégradé / Close-up of colours and gradient
- [ ] Kangourou d’équipe avec impression au dos / Team hoodie with a back print

## Broderie / Embroidery (3 photos)

- [ ] Logo brodé sur polo, gros plan / Embroidered logo on a polo, close-up
- [ ] Casquette brodée vue de face / Embroidered cap, front view
- [ ] Uniformes brodés portés par une équipe / Embroidered uniforms worn by a team

## Lettrage en vinyle / Vinyl lettering (3 photos)

- [ ] Vitrine de commerce avec lettrage posé / Storefront window with installed lettering
- [ ] Véhicule de service avec logo en vinyle / Service vehicle with vinyl logo
- [ ] Pose du vinyle en cours (mains et outils) / Vinyl being installed (hands and tools)

## Enseignes / Signage (3 photos)

- [ ] Enseigne installée sur une façade / Sign installed on a storefront
- [ ] Présentoir promotionnel dans un commerce / Promotional display in a shop
- [ ] Détail de finition d’une enseigne / Finishing detail of a sign

## Produits promotionnels / Promotional products (3 photos)

- [ ] Ensemble d’articles promotionnels avec logo / Set of branded promotional items
- [ ] Cadeau d’entreprise emballé / Wrapped corporate gift
- [ ] Table d’événement avec marchandise / Event table with merchandise

## Impression pour événements / Event printing (3 photos)

- [ ] Monogramme posé sur une piste de danse / Monogram on a dance floor
- [ ] Affichage d’accueil d’un mariage / Wedding welcome signage
- [ ] T-shirts d’un tournoi ou d’une collecte de fonds / Tournament or fundraiser T-shirts

## Conception graphique / Graphic design (3 photos)

- [ ] Avant / après d’un logo vectorisé / Before / after of a vectorized logo
- [ ] Maquette d’un t-shirt avec logo / Mockup of a T-shirt with a logo
- [ ] Écran de travail avec un fichier vectoriel / Workstation with a vector file

## Also useful

- [ ] The owner or team at work (About section; builds trust more than any sentence)
- [ ] The workshop or equipment, only as it really is
- [ ] Before / after of a storefront window

## Adding photos to the site

1. Put the files in `assets/images/work/` (for example `polos-brodes.jpg`).
2. Add one entry per photo to `PORTFOLIO` in `tools/content.py` (file, service, French and English caption, width, height). The format is shown in that file.
3. Run `python3 tools/build.py`. Photos appear on the home page and on their service page, in place of the Instagram panel.
