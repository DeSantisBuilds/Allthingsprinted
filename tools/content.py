# -*- coding: utf-8 -*-
"""
All Things Printed — site content (French first, English second).

Every fact here comes from the owner (business overview of 2026-11-22 and later
answers). Do NOT add prices, minimum quantities, equipment, client names,
reviews or turnaround promises that the owner has not confirmed.

After editing, rebuild the site:  python3 tools/build.py
"""

SITE = {
    "domain": "https://allthingsprinted.ca",  # canonical host (www redirects here)
    "name": "All Things Printed",
    "legal_hint": "ATP Inc.",
    "phone_e164": "+15148151829",
    "phone_fr": "514 815-1829",
    "phone_en": "(514) 815-1829",
    "email": "info@allthingsprinted.ca",
    "instagram": "https://www.instagram.com/allthingsprintedinc/",
    "instagram_handle": "@allthingsprintedinc",
    # FormSubmit (formsubmit.co) delivers the quote form. Replace the address in
    # "form_action" with the FormSubmit alias once it is activated.
    "form_action": "https://formsubmit.co/info@allthingsprinted.ca",
    "form_sms_cc": "5148151829@txt.bell.ca",
}

# Facts the owner confirmed (used in the FAQ, hero chips and process steps).
FACTS = {
    "fr": {
        "turnaround": "10 à 15 jours ouvrables",
        "hours": "Du lundi au samedi, de 9&nbsp;h à 17&nbsp;h",
        "hours_short": "Lun.–sam., 9&nbsp;h–17&nbsp;h",
        "area": "Grand Montréal",
    },
    "en": {
        "turnaround": "10 to 15 business days",
        "hours": "Monday to Saturday, 9&nbsp;a.m. to 5&nbsp;p.m.",
        "hours_short": "Mon–Sat, 9&nbsp;a.m.–5&nbsp;p.m.",
        "area": "Greater Montreal",
    },
}

# Quote-form "service" choices, in order. Keys match SERVICES[*]["key"].
FORM_SERVICES = ["apparel", "dtf", "embroidery", "vinyl", "signage", "promo", "events", "design"]

# Apparel products (owner's list). Keys are used by the garment rail.
GARMENTS = [
    {"key": "tshirt", "fr": "T-shirts", "en": "T-shirts", "ink": "g-c"},
    {"key": "longsleeve", "fr": "Manches longues", "en": "Long sleeves", "ink": "g-k"},
    {"key": "hoodie", "fr": "Kangourous et cotons ouatés", "en": "Hoodies and sweatshirts", "ink": "g-y"},
    {"key": "polo", "fr": "Polos", "en": "Polos", "ink": "g-w"},
    {"key": "workwear", "fr": "Vêtements de travail et uniformes", "en": "Workwear and uniforms", "ink": "g-c"},
    {"key": "team", "fr": "Vêtements d’équipe et d’événement", "en": "Team and event apparel", "ink": "g-m"},
    {"key": "cap", "fr": "Casquettes et tuques", "en": "Caps and tuques", "ink": "g-y"},
]

# Who we serve (owner's target customers).
INDUSTRIES = {
    "smb": {"fr": ("PME", "Uniformes, vêtements à votre image, enseignes et matériel promotionnel."),
            "en": ("Small and medium businesses", "Uniforms, branded apparel, signage and promotional materials.")},
    "corporate": {"fr": ("Entreprises", "Vêtements professionnels pour employés, cadeaux d’entreprise et marchandise à votre image."),
                  "en": ("Corporate clients", "Professional employee apparel, corporate gifts and branded merchandise.")},
    "trades": {"fr": ("Entrepreneurs et métiers", "Vêtements de travail à votre image pour la construction, l’automobile et les services."),
               "en": ("Contractors and trades", "Branded workwear for construction, automotive and service businesses.")},
    "hospitality": {"fr": ("Restauration et hôtellerie", "Uniformes, marchandise et impression promotionnelle pour restaurants et cafés."),
                    "en": ("Restaurants and hospitality", "Uniforms, merchandise and promotional printing for restaurants and cafés.")},
    "events": {"fr": ("Événements et organismes", "Mariages, tournois, collectes de fonds, événements communautaires et d’entreprise."),
               "en": ("Events and organizations", "Weddings, tournaments, fundraisers, community and corporate events.")},
    "individuals": {"fr": ("Particuliers", "Vêtements personnalisés et projets d’impression uniques."),
                    "en": ("Individuals", "Personalized apparel and one-of-a-kind printing projects.")},
}

# Owner-confirmed answers, reused across pages.
FAQ_BANK = {
    "turnaround": {
        "fr": ("Combien de temps faut-il pour une commande&nbsp;?", "Le délai habituel est de 10 à 15 jours ouvrables. Si vous avez une date limite, indiquez-la dans votre demande."),
        "en": ("How long does an order take?", "Typical turnaround is 10 to 15 business days. If you have a deadline, include it in your request."),
    },
    "files": {
        "fr": ("Quel fichier dois-je envoyer&nbsp;?", "Un fichier vectoriel (AI, EPS, SVG ou PDF vectoriel) est idéal. Si votre fichier n’est pas vectorisé, nous pouvons l’ajuster&nbsp;; des frais s’appliquent pour cet ajustement."),
        "en": ("What file should I send?", "A vector file (AI, EPS, SVG or vector PDF) is best. If your file isn’t vectorized, we can adjust it; a fee applies for the adjustment."),
    },
    "mockup": {
        "fr": ("Vais-je voir mon design avant l’impression&nbsp;?", "Oui. La maquette visuelle est incluse dans le prix et vous est envoyée une fois la soumission approuvée."),
        "en": ("Will I see my design before printing?", "Yes. The visual mockup is included in the price and sent to you once your quote is approved."),
    },
    "payment": {
        "fr": ("Comment fonctionne le paiement&nbsp;?", "Un dépôt de 50&nbsp;% confirme la commande et le solde de 50&nbsp;% est payable à la fin."),
        "en": ("How does payment work?", "A 50% deposit confirms the order, and the remaining 50% is due on completion."),
    },
    "delivery": {
        "fr": ("Offrez-vous la livraison&nbsp;?", "Oui, dans le Grand Montréal. Des frais de livraison peuvent s’appliquer selon la commande et l’endroit."),
        "en": ("Do you deliver?", "Yes, in Greater Montreal. Delivery fees may apply depending on the order and location."),
    },
    "artwork": {
        "fr": ("Comment vous envoyer mon logo&nbsp;?", "Envoyez d’abord votre demande avec le formulaire, puis écrivez-nous à info@allthingsprinted.ca avec votre fichier en pièce jointe et votre nom en objet. Vous n’avez pas de fichier&nbsp;? Choisissez «&nbsp;J’ai besoin d’aide&nbsp;» dans le formulaire."),
        "en": ("How do I send you my logo?", "Send your request with the form first, then email info@allthingsprinted.ca with your file attached and your name in the subject. No file yet? Choose “I need help” in the form."),
    },
    "reorder": {
        "fr": ("Comment recommander le même article&nbsp;?", "Choisissez «&nbsp;Recommande&nbsp;» dans le formulaire et décrivez votre commande précédente (produit, date approximative). Cela nous aide à préparer votre soumission plus rapidement."),
        "en": ("How do I reorder the same item?", "Choose “Reorder” in the form and describe your previous order (product, approximate date). It helps us prepare your quote faster."),
    },
}

# ---------------------------------------------------------------------------
# Services. "shots" are the photos to take for each page (see the photography
# shot list); until real photos exist they are only shown, clearly labelled,
# in the development preview.
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "key": "apparel", "icon": "apparel", "ink": "c",
        "slug": {"fr": "vetements-personnalises", "en": "custom-apparel"},
        "fr": {
            "name": "Vêtements personnalisés",
            "card": "T-shirts, kangourous, polos, uniformes et casquettes à votre image.",
            "h1": "Vêtements personnalisés à Montréal",
            "title": "Vêtements personnalisés à Montréal | All Things Printed",
            "desc": "T-shirts, kangourous, polos, uniformes et casquettes personnalisés pour entreprises, équipes et événements du Grand Montréal. Soumission gratuite.",
            "lead": "Des vêtements à votre image pour vos employés, votre équipe, votre événement ou votre projet personnel, décorés par impression DTF, vinyle thermocollant ou broderie.",
            "intro": [
                "Nous transformons votre logo ou votre design en vêtements de qualité. Vous ne savez pas quelle technique choisir&nbsp;? Nous vous recommandons la mieux adaptée à votre design et au vêtement.",
            ],
            "options_title": "Vêtements offerts",
            "options": ["T-shirts", "Chandails à manches longues", "Kangourous et cotons ouatés", "Polos", "Vêtements de travail et uniformes", "Casquettes, chapeaux et tuques", "Vêtements d’équipe et d’événement"],
            "apps_title": "Techniques de décoration",
            "apps": ["<strong>Impression DTF</strong>&nbsp;: graphiques détaillés et multicolores", "<strong>Vinyle thermocollant (HTV)</strong>&nbsp;: lettrage, noms et numéros", "<strong>Broderie</strong>&nbsp;: fini haut de gamme pour polos, casquettes et uniformes"],
        },
        "en": {
            "name": "Custom apparel",
            "card": "T-shirts, hoodies, polos, uniforms and hats with your brand.",
            "h1": "Custom apparel in Montreal",
            "title": "Custom Apparel Printing in Montreal | All Things Printed",
            "desc": "Custom T-shirts, hoodies, polos, uniforms and hats for Greater Montreal businesses, teams and events. Free quote.",
            "lead": "Branded clothing for your employees, team, event or personal project, decorated with DTF printing, heat transfer vinyl or embroidery.",
            "intro": [
                "We turn your logo or design into quality apparel. Not sure which method to choose? We’ll recommend the best fit for your design and garment.",
            ],
            "options_title": "Garments we offer",
            "options": ["T-shirts", "Long-sleeve shirts", "Hoodies and sweatshirts", "Polo shirts", "Workwear and uniforms", "Hats, caps and tuques", "Team and event apparel"],
            "apps_title": "Decoration methods",
            "apps": ["<strong>DTF printing</strong>: detailed, multicolour graphics", "<strong>Heat transfer vinyl (HTV)</strong>: lettering, names and numbers", "<strong>Embroidery</strong>: a premium finish for polos, hats and uniforms"],
        },
        "industries": ["smb", "corporate", "trades", "hospitality", "events", "individuals"],
        "faq": ["turnaround", "files", "mockup", "reorder"],
        "related": ["dtf", "embroidery", "design"],
        "garments": True,
        "shots": {"fr": ["Pile de t-shirts imprimés, logo bien visible", "Employé portant un polo brodé (de face)", "Détail rapproché d’une impression DTF"],
                  "en": ["Stack of printed T-shirts, logo clearly visible", "Employee wearing an embroidered polo (front)", "Close-up of a DTF print"]},
    },
    {
        "key": "dtf", "icon": "dtf", "ink": "m",
        "slug": {"fr": "impression-dtf", "en": "dtf-printing"},
        "fr": {
            "name": "Impression DTF",
            "card": "Graphiques détaillés et multicolores sur vos vêtements.",
            "h1": "Impression DTF à Montréal",
            "title": "Impression DTF sur vêtements à Montréal | All Things Printed",
            "desc": "Impression DTF (direct sur film) pour des designs détaillés et multicolores sur t-shirts, kangourous et vêtements d’équipe. Grand Montréal.",
            "lead": "L’impression DTF (direct sur film) est une méthode polyvalente pour reproduire des graphiques détaillés et multicolores sur vos vêtements.",
            "intro": [
                "Votre design est imprimé sur un film, puis appliqué sur le vêtement à la presse à chaud. C’est le bon choix pour les logos en couleur, les dégradés et les illustrations détaillées.",
            ],
            "options_title": "Idéal pour",
            "options": ["Logos et designs multicolores", "Dégradés et illustrations détaillées", "T-shirts et chandails à manches longues", "Kangourous et cotons ouatés", "Vêtements d’équipe et d’événement"],
            "apps_title": "Bon à savoir",
            "apps": ["Pour des noms ou des numéros d’une seule couleur, le vinyle thermocollant est souvent plus simple.", "Pour un look haut de gamme sur polos et casquettes, pensez à la broderie.", "Nous vous conseillons la meilleure technique lors de la soumission."],
        },
        "en": {
            "name": "DTF printing",
            "card": "Detailed, multicolour graphics on your garments.",
            "h1": "DTF printing in Montreal",
            "title": "DTF Printing on Apparel in Montreal | All Things Printed",
            "desc": "DTF (direct-to-film) printing for detailed, multicolour designs on T-shirts, hoodies and team apparel in Greater Montreal.",
            "lead": "DTF (direct-to-film) printing is a versatile method for producing detailed, multicolour graphics on garments.",
            "intro": [
                "Your design is printed onto a film, then heat-pressed onto the garment. It is the right choice for full-colour logos, gradients and detailed artwork.",
            ],
            "options_title": "Best for",
            "options": ["Multicolour logos and designs", "Gradients and detailed artwork", "T-shirts and long sleeves", "Hoodies and sweatshirts", "Team and event apparel"],
            "apps_title": "Good to know",
            "apps": ["For one-colour names or numbers, heat transfer vinyl is often simpler.", "For a premium look on polos and hats, consider embroidery.", "We recommend the best method when we prepare your quote."],
        },
        "industries": ["smb", "events", "individuals"],
        "faq": ["files", "mockup", "turnaround"],
        "related": ["apparel", "embroidery", "design"],
        "shots": {"fr": ["Design multicolore imprimé en DTF sur un t-shirt foncé", "Détail rapproché des couleurs et du dégradé", "Kangourou d’équipe avec impression au dos"],
                  "en": ["Multicolour DTF design on a dark T-shirt", "Close-up of colours and gradient", "Team hoodie with a back print"]},
    },
    {
        "key": "embroidery", "icon": "embroidery", "ink": "y",
        "slug": {"fr": "broderie", "en": "embroidery"},
        "fr": {
            "name": "Broderie",
            "card": "Un fini haut de gamme pour polos, casquettes et uniformes.",
            "h1": "Broderie de vêtements à Montréal",
            "title": "Broderie de vêtements à Montréal | All Things Printed",
            "desc": "Broderie de logos sur polos, casquettes, uniformes et vêtements corporatifs pour entreprises du Grand Montréal. Soumission gratuite.",
            "lead": "La broderie donne un fini texturé et haut de gamme à vos vêtements d’entreprise&nbsp;: polos, casquettes, uniformes et vêtements corporatifs.",
            "intro": [
                "Votre logo est brodé directement dans le tissu. C’est l’option idéale pour une image professionnelle et durable auprès de vos clients.",
            ],
            "options_title": "Vêtements courants",
            "options": ["Polos", "Casquettes et tuques", "Uniformes", "Vêtements corporatifs"],
            "apps_title": "Idéal pour",
            "apps": ["Logos et textes courts", "Image professionnelle pour le personnel", "Vêtements d’entreprise haut de gamme"],
        },
        "en": {
            "name": "Embroidery",
            "card": "A premium finish for polos, hats and uniforms.",
            "h1": "Embroidery in Montreal",
            "title": "Custom Embroidery in Montreal | All Things Printed",
            "desc": "Logo embroidery on polos, hats, uniforms and corporate clothing for Greater Montreal businesses. Visual mockup included. Free quote.",
            "lead": "Embroidery gives your business apparel a textured, premium finish: polos, hats, uniforms and corporate clothing.",
            "intro": [
                "Your logo is stitched directly into the fabric. It is the ideal option for a professional, lasting image in front of your customers.",
            ],
            "options_title": "Common garments",
            "options": ["Polo shirts", "Caps and tuques", "Uniforms", "Corporate clothing"],
            "apps_title": "Best for",
            "apps": ["Logos and short text", "A professional look for staff", "Premium corporate apparel"],
        },
        "industries": ["corporate", "smb", "hospitality", "trades"],
        "faq": ["files", "mockup", "turnaround"],
        "related": ["apparel", "dtf", "promo"],
        "shots": {"fr": ["Logo brodé sur polo, gros plan", "Casquette brodée vue de face", "Uniformes brodés portés par une équipe"],
                  "en": ["Embroidered logo on a polo, close-up", "Embroidered cap, front view", "Embroidered uniforms worn by a team"]},
    },
    {
        "key": "vinyl", "icon": "vinyl", "ink": "m",
        "slug": {"fr": "lettrage-vinyle", "en": "vinyl-lettering"},
        "fr": {
            "name": "Lettrage en vinyle",
            "card": "Vitrines, murs, véhicules et décalques à votre image.",
            "h1": "Lettrage en vinyle à Montréal",
            "title": "Lettrage vinyle et vitrines à Montréal | All Things Printed",
            "desc": "Lettrage en vinyle, graphiques de vitrine, décalques muraux et de véhicules pour commerces du Grand Montréal. Pose soignée. Soumission gratuite.",
            "lead": "Lettrage et graphiques en vinyle pour une image de marque nette et professionnelle, avec une pose soignée et précise.",
            "intro": [
                "Le lettrage et les graphiques sont découpés dans du vinyle adhésif, puis posés sur la surface. Indiquez l’emplacement, la surface et les dimensions dans votre demande.",
            ],
            "options_title": "Ce que nous réalisons",
            "options": ["Lettrage en vinyle personnalisé", "Graphiques de vitrine", "Image de marque de façade", "Décalques et graphiques muraux", "Décalques et graphiques de véhicules", "Vinyle décoratif"],
            "apps_title": "Exemples d’utilisation",
            "apps": ["Nom, heures et coordonnées sur votre vitrine", "Logo sur un véhicule de service", "Décor mural dans un commerce ou un bureau"],
        },
        "en": {
            "name": "Vinyl lettering",
            "card": "Windows, walls, vehicles and decals with your brand.",
            "h1": "Vinyl lettering in Montreal",
            "title": "Vinyl Lettering & Window Graphics in Montreal | ATP",
            "desc": "Vinyl lettering, window graphics, wall and vehicle decals for Greater Montreal businesses, with careful installation. Free quote.",
            "lead": "Vinyl lettering and graphics for clean, professional branding, with careful and accurate installation.",
            "intro": [
                "Lettering and graphics are cut from adhesive vinyl and applied to the surface. Tell us the location, surface and size in your request.",
            ],
            "options_title": "What we make",
            "options": ["Custom vinyl lettering", "Window graphics", "Storefront branding", "Wall decals and graphics", "Vehicle decals and graphics", "Decorative vinyl"],
            "apps_title": "Example uses",
            "apps": ["Name, hours and contact details on your window", "Logo on a service vehicle", "Wall decor in a shop or office"],
        },
        "industries": ["smb", "hospitality", "trades", "corporate"],
        "faq": ["files", "mockup", "turnaround"],
        "related": ["signage", "events", "design"],
        "shots": {"fr": ["Vitrine de commerce avec lettrage posé", "Véhicule de service avec logo en vinyle", "Pose du vinyle en cours (mains et outils)"],
                  "en": ["Storefront window with installed lettering", "Service vehicle with vinyl logo", "Vinyl being installed (hands and tools)"]},
    },
    {
        "key": "signage", "icon": "signage", "ink": "k",
        "slug": {"fr": "enseignes", "en": "signage"},
        "fr": {
            "name": "Enseignes",
            "card": "Enseignes commerciales et présentoirs promotionnels.",
            "h1": "Enseignes commerciales à Montréal",
            "title": "Enseignes commerciales à Montréal | All Things Printed",
            "desc": "Enseignes commerciales, présentoirs promotionnels et image de marque de façade pour entreprises du Grand Montréal. Soumission gratuite.",
            "lead": "Des enseignes et des présentoirs qui rendent votre entreprise visible et professionnelle.",
            "intro": [
                "Pour une soumission précise, indiquez les dimensions souhaitées, l’emplacement (intérieur ou extérieur) et la surface de pose.",
            ],
            "options_title": "Ce que nous réalisons",
            "options": ["Enseignes commerciales", "Présentoirs promotionnels", "Image de marque de façade", "Graphiques de vitrine"],
            "apps_title": "Pour",
            "apps": ["Commerces et bureaux", "Restaurants et cafés", "Événements et salons"],
        },
        "en": {
            "name": "Signage",
            "card": "Business signs and promotional displays.",
            "h1": "Business signage in Montreal",
            "title": "Business Signage in Montreal | All Things Printed",
            "desc": "Business signage, promotional displays and storefront branding for shops, offices and restaurants in Greater Montreal. Free quote.",
            "lead": "Signs and displays that make your business visible and professional.",
            "intro": [
                "For an accurate quote, tell us the size you want, the location (indoor or outdoor) and the mounting surface.",
            ],
            "options_title": "What we make",
            "options": ["Business signage", "Promotional displays", "Storefront branding", "Window graphics"],
            "apps_title": "For",
            "apps": ["Shops and offices", "Restaurants and cafés", "Events and trade shows"],
        },
        "industries": ["smb", "hospitality", "corporate", "events"],
        "faq": ["files", "mockup", "turnaround"],
        "related": ["vinyl", "promo", "design"],
        "shots": {"fr": ["Enseigne installée sur une façade", "Présentoir promotionnel dans un commerce", "Détail de finition d’une enseigne"],
                  "en": ["Sign installed on a storefront", "Promotional display in a shop", "Finishing detail of a sign"]},
    },
    {
        "key": "promo", "icon": "promo", "ink": "y",
        "slug": {"fr": "produits-promotionnels", "en": "promotional-products"},
        "fr": {
            "name": "Produits promotionnels",
            "card": "Articles et cadeaux d’entreprise à votre image.",
            "h1": "Produits promotionnels à Montréal",
            "title": "Produits promotionnels à Montréal | All Things Printed",
            "desc": "Articles promotionnels, cadeaux d’entreprise et marchandise d’événement personnalisés pour entreprises du Grand Montréal. Soumission gratuite.",
            "lead": "De la marchandise personnalisée qui garde votre marque bien en vue auprès de vos clients, employés et invités.",
            "intro": [
                "La disponibilité des produits varie selon le projet&nbsp;: dites-nous ce que vous cherchez, la quantité et la date souhaitée, et nous vous confirmerons les options.",
            ],
            "options_title": "Catégories",
            "options": ["Articles pour boissons", "Accessoires promotionnels", "Cadeaux d’entreprise", "Marchandise d’événement", "Articles promotionnels à distribuer", "Produits d’affaires personnalisés"],
            "apps_title": "Occasions",
            "apps": ["Cadeaux pour clients et employés", "Salons et événements d’entreprise", "Lancements et promotions"],
        },
        "en": {
            "name": "Promotional products",
            "card": "Branded items and corporate gifts.",
            "h1": "Promotional products in Montreal",
            "title": "Promotional Products in Montreal | All Things Printed",
            "desc": "Branded promotional items, corporate gifts and event merchandise for Greater Montreal businesses, clients and employees. Free quote.",
            "lead": "Customized merchandise that keeps your brand in front of clients, employees and guests.",
            "intro": [
                "Product availability varies by project: tell us what you’re looking for, the quantity and your date, and we’ll confirm the options.",
            ],
            "options_title": "Categories",
            "options": ["Branded drinkware", "Promotional accessories", "Corporate gifts", "Event merchandise", "Custom giveaways", "Personalized business products"],
            "apps_title": "Occasions",
            "apps": ["Gifts for clients and employees", "Trade shows and corporate events", "Launches and promotions"],
        },
        "industries": ["corporate", "smb", "events"],
        "faq": ["turnaround", "files", "delivery"],
        "related": ["apparel", "events", "embroidery"],
        "shots": {"fr": ["Ensemble d’articles promotionnels avec logo", "Cadeau d’entreprise emballé", "Table d’événement avec marchandise"],
                  "en": ["Set of branded promotional items", "Wrapped corporate gift", "Event table with merchandise"]},
    },
    {
        "key": "events", "icon": "events", "ink": "c",
        "slug": {"fr": "impression-evenements", "en": "event-printing"},
        "fr": {
            "name": "Impression pour événements",
            "card": "Mariages, célébrations et événements d’entreprise.",
            "h1": "Impression pour mariages et événements à Montréal",
            "title": "Impression pour mariages et événements | Montréal | ATP",
            "desc": "Monogrammes de piste de danse, décalques, affichage et vêtements pour mariages, célébrations et événements d’entreprise du Grand Montréal.",
            "lead": "Impression personnalisée pour les mariages, les célébrations, les événements d’entreprise et les occasions spéciales.",
            "intro": [
                "Prévoyez votre demande à l’avance&nbsp;: le délai habituel est de 10 à 15 jours ouvrables. Indiquez la date de l’événement dans le formulaire.",
            ],
            "options_title": "Ce que nous réalisons",
            "options": ["Monogrammes de piste de danse", "Décalques personnalisés", "Affichage d’événement", "Vêtements d’événement", "Lettrage décoratif", "Matériel d’événement à votre image"],
            "apps_title": "Occasions",
            "apps": ["Mariages", "Anniversaires et célébrations", "Événements d’entreprise", "Tournois et collectes de fonds"],
        },
        "en": {
            "name": "Event printing",
            "card": "Weddings, celebrations and corporate events.",
            "h1": "Wedding and event printing in Montreal",
            "title": "Wedding & Event Printing in Montreal | All Things Printed",
            "desc": "Dance floor monograms, decals, signage and apparel for weddings, celebrations and corporate events in Greater Montreal.",
            "lead": "Personalized printing for weddings, celebrations, corporate events and special occasions.",
            "intro": [
                "Plan ahead: typical turnaround is 10 to 15 business days. Include your event date in the form.",
            ],
            "options_title": "What we make",
            "options": ["Wedding dance floor monograms", "Personalized decals", "Event signage", "Custom event apparel", "Decorative lettering", "Branded event materials"],
            "apps_title": "Occasions",
            "apps": ["Weddings", "Birthdays and celebrations", "Corporate events", "Tournaments and fundraisers"],
        },
        "industries": ["events", "corporate", "individuals"],
        "faq": ["turnaround", "mockup", "delivery"],
        "related": ["vinyl", "apparel", "promo"],
        "shots": {"fr": ["Monogramme posé sur une piste de danse", "Affichage d’accueil d’un mariage", "T-shirts d’un tournoi ou d’une collecte de fonds"],
                  "en": ["Monogram on a dance floor", "Wedding welcome signage", "Tournament or fundraiser T-shirts"]},
    },
    {
        "key": "design", "icon": "design", "ink": "k",
        "slug": {"fr": "conception-graphique", "en": "graphic-design"},
        "fr": {
            "name": "Conception graphique",
            "card": "Préparation de logo, vectorisation et maquettes.",
            "h1": "Conception et préparation de fichiers d’impression",
            "title": "Vectorisation et préparation de logo | All Things Printed",
            "desc": "Préparation de logo, nettoyage, vectorisation, fichiers prêts à imprimer et maquettes de production. Envoyez votre visuel ou demandez de l’aide.",
            "lead": "Envoyez le visuel que vous avez, ou demandez-nous de vous aider à le préparer pour l’impression.",
            "intro": [
                "Nous nous assurons que votre design est bien dimensionné, bien positionné et prêt pour la production. Les fichiers vectoriels sont prêts à imprimer&nbsp;; l’ajustement des autres fichiers entraîne des frais.",
            ],
            "options_title": "Services",
            "options": ["Préparation de logo", "Nettoyage de visuels", "Vectorisation", "Fichiers prêts à imprimer", "Mise en page graphique", "Dimensionnement et positionnement", "Maquettes de production", "Concepts de marque"],
            "apps_title": "Quand en avoir besoin",
            "apps": ["Votre logo n’existe qu’en JPG ou en PNG", "Vous avez une idée, mais pas encore de design", "Vous voulez voir le résultat avant de commander"],
        },
        "en": {
            "name": "Graphic design",
            "card": "Logo preparation, vectorization and mockups.",
            "h1": "Design and print-ready file preparation",
            "title": "Logo Vectorization & Print-Ready Files | All Things Printed",
            "desc": "Logo preparation, cleanup, vectorization, print-ready files and production mockups. Send your artwork or ask for help.",
            "lead": "Send the artwork you have, or ask us to help prepare it for printing.",
            "intro": [
                "We make sure your design is sized, positioned and ready for production. Vector files are print-ready; adjusting other files carries a fee.",
            ],
            "options_title": "Services",
            "options": ["Logo preparation", "Artwork cleanup", "Vectorization", "Print-ready file preparation", "Graphic layout", "Sizing and positioning", "Production mockups", "Branding concepts"],
            "apps_title": "When you need it",
            "apps": ["Your logo only exists as a JPG or PNG", "You have an idea but no design yet", "You want to see the result before ordering"],
        },
        "industries": ["smb", "individuals", "events"],
        "faq": ["files", "mockup", "artwork"],
        "related": ["apparel", "vinyl", "signage"],
        "shots": {"fr": ["Avant / après d’un logo vectorisé", "Maquette d’un t-shirt avec logo", "Écran de travail avec un fichier vectoriel"],
                  "en": ["Before / after of a vectorized logo", "Mockup of a T-shirt with a logo", "Workstation with a vector file"]},
    },
]

# Home-page portfolio slots (shown only in the development preview until real
# photos are added to PORTFOLIO below).
HOME_SHOTS = {
    "fr": ["Commande de t-shirts d’entreprise", "Vitrine lettrée", "Polos brodés", "Kangourous d’équipe", "Monogramme de mariage", "Articles promotionnels"],
    "en": ["Corporate T-shirt order", "Lettered storefront", "Embroidered polos", "Team hoodies", "Wedding monogram", "Promotional items"],
}

# Real photos of completed work. Add entries like:
#   {"file": "assets/images/work/polos-brodes.jpg", "service": "embroidery",
#    "fr": "Polos brodés pour une équipe", "en": "Embroidered polos for a team",
#    "width": 1200, "height": 900}
# The file must show real work by All Things Printed.
PORTFOLIO = []

# Optional seasonal banner. Off in production until "enabled" is True. The
# preview shows it, labelled as an example.
SEASONAL = {
    "enabled": False,
    "service": "promo",
    "fr": ("Cadeaux d’entreprise des Fêtes", "Planifiez vos cadeaux pour clients et employés&nbsp;: prévoyez 10 à 15 jours ouvrables.", "Demander une soumission"),
    "en": ("Holiday corporate gifts", "Plan your gifts for clients and employees: allow 10 to 15 business days.", "Request a quote"),
}
