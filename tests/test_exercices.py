"""Tests des corrigés (et NON des fichiers mes_essais). Exécution: python -m unittest discover -s tests -v"""
import importlib
import importlib.util
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path


def solution(n, slug):
    return importlib.import_module(f'exercices.ex{n:02d}_{slug}.solution')


class Ex01Etudiant(unittest.TestCase):
    def setUp(self): self.m = solution(1, 'etudiant')
    def test_moyenne_et_admission(self):
        e = self.m.Etudiant(' Kasongo ', 'Amina')
        for v in (12, 14, 10): e.ajouter_note(v)
        self.assertEqual(e.moyenne(), 12)
        self.assertTrue(e.est_admis())
        self.assertEqual(e.nom, 'Kasongo')
    def test_notes_vides(self):
        e = self.m.Etudiant('A', 'B')
        self.assertIsNone(e.moyenne())
        self.assertFalse(e.est_admis())
    def test_notes_invalides(self):
        e = self.m.Etudiant('A', 'B')
        for x in (-1, 21, True):
            with self.subTest(x=x), self.assertRaises(ValueError): e.ajouter_note(x)
    def test_instances_independantes(self):
        x, y = self.m.Etudiant('A','B'), self.m.Etudiant('C','D')
        x.ajouter_note(10)
        self.assertEqual(y.notes, [])


class Ex02Rectangle(unittest.TestCase):
    def setUp(self): self.m = solution(2, 'rectangle')
    def test_mesures(self):
        r = self.m.Rectangle(3,4)
        self.assertEqual((r.surface,r.perimetre), (12,14))
    def test_redimensionnement_atomique(self):
        r = self.m.Rectangle(3,4)
        with self.assertRaises(ValueError): r.redimensionner(10,-5)
        self.assertEqual((r.largeur,r.hauteur), (3,4))
    def test_propriete_protegee(self):
        r = self.m.Rectangle(2,2)
        with self.assertRaises(AttributeError): r.largeur = -5
    def test_zero_interdit(self):
        with self.assertRaises(ValueError): self.m.Rectangle(0,5)


class Ex03Compte(unittest.TestCase):
    def setUp(self): self.m = solution(3, 'compte')
    def test_transfert_conservation(self):
        a,b = self.m.CompteBancaire('A',100),self.m.CompteBancaire('B')
        a.transferer(b,35)
        self.assertEqual((a.solde,b.solde),(Decimal('65'),Decimal('35')))
    def test_retrait_refuse_sans_mutation(self):
        a = self.m.CompteBancaire('A',5)
        with self.assertRaises(ValueError): a.retirer(6)
        self.assertEqual(a.solde,5)
    def test_depot(self):
        a = self.m.CompteBancaire('A')
        a.deposer('0.1')
        a.deposer('0.2')
        self.assertEqual(a.solde, Decimal('0.3'))
    def test_transfert_soi_meme_et_zero(self):
        a,b = self.m.CompteBancaire('A',100), self.m.CompteBancaire('B')
        with self.assertRaises(ValueError): a.transferer(a,5)
        with self.assertRaises(ValueError): a.transferer(b,0)


class Ex04Produit(unittest.TestCase):
    def setUp(self): self.m = solution(4,'produit')
    def test_fabrique(self):
        p = self.m.Produit.depuis_ligne('P01;Clavier;25')
        self.assertEqual((p.code,p.nom,p.prix_ht),('P01','Clavier',25))
    def test_taxe(self):
        self.assertEqual(self.m.Produit.prix_ttc(25),Decimal('29.00'))
    def test_ligne_invalide(self):
        with self.assertRaises(ValueError): self.m.Produit.depuis_ligne('P01;Clavier')
    def test_prix_invalide(self):
        with self.assertRaises(ValueError): self.m.Produit('A','Stylo',-2)
    def test_representation(self):
        self.assertIn('Clavier',repr(self.m.Produit('A','Clavier',1)))


class Ex05Panier(unittest.TestCase):
    def setUp(self): self.m=solution(5,'panier')
    def test_total(self):
        p=self.m.Panier()
        p.ajouter(self.m.Article('A','Stylo','2.5'),3)
        p.ajouter(self.m.Article('B','Cahier',4),2)
        self.assertEqual(p.total(),Decimal('15.5'))
    def test_cumul_et_retrait(self):
        p=self.m.Panier()
        p.ajouter(self.m.Article('A','Stylo',2),2)
        p.ajouter(self.m.Article('A','Stylo',2),2)
        p.retirer('A',3)
        self.assertEqual(p.lignes()[0][1],1)
        p.retirer('A')
        self.assertEqual(p.total(),0)
    def test_produit_incoherent(self):
        p=self.m.Panier()
        p.ajouter(self.m.Article('A','Stylo',2))
        with self.assertRaises(ValueError): p.ajouter(self.m.Article('A','Stylo',3))
    def test_retrait_trop_important(self):
        with self.assertRaises(ValueError): self.m.Panier().retirer('A')


class Ex06Personnel(unittest.TestCase):
    def setUp(self): self.m=solution(6,'personnel')
    def test_polymorphisme(self):
        e=[self.m.Salarie('A',1000),self.m.Freelance('B',20,15)]
        self.assertEqual(self.m.masse_salariale(e),1300)
    def test_vide(self): self.assertEqual(self.m.masse_salariale([]),0)
    def test_heures_invalides(self):
        with self.assertRaises(ValueError): self.m.Freelance('A',-1,5)
    def test_super(self): self.assertEqual(self.m.Salarie(' A ',200).nom,'A')


class Ex07Paiement(unittest.TestCase):
    def setUp(self): self.m=solution(7,'paiements')
    def test_cb(self):
        self.assertEqual(self.m.Caisse().encaisser(self.m.Carte('1234'),20),'CB-1234-20.00')
    def test_paiement_autres_types(self):
        c=self.m.Caisse()
        self.assertEqual(c.encaisser(self.m.Especes(),5),'CASH-5.00')
        self.assertIn('MOMO-',c.encaisser(self.m.MobileMoney('2438900001'),5))
    def test_abstraction(self):
        with self.assertRaises(TypeError): self.m.MoyenPaiement()
    def test_montant_invalide(self):
        with self.assertRaises(ValueError): self.m.Caisse().encaisser(self.m.Especes(),0)
    def test_carte_invalide(self):
        with self.assertRaises(ValueError): self.m.Carte('hello')


class Ex08Stock(unittest.TestCase):
    def setUp(self): self.m=solution(8,'stock')
    def test_mouvement(self):
        a,b=self.m.Stock(),self.m.Stock()
        a.ajouter('P',10)
        a.transferer(b,'P',4)
        self.assertEqual((a.quantite('P'),b.quantite('P')),(6,4))
    def test_exception_specifique(self):
        s=self.m.Stock()
        with self.assertRaises(self.m.ReferenceInconnue): s.sortir('x',1)
    def test_insuffisant_pas_mutation(self):
        a,b=self.m.Stock(),self.m.Stock()
        a.ajouter('P',3)
        with self.assertRaises(self.m.StockInsuffisant): a.transferer(b,'P',4)
        self.assertEqual((a.quantite('P'),b.quantite('P')),(3,0))
    def test_quantite_invalide(self):
        with self.assertRaises(ValueError): self.m.Stock().ajouter('X',0)


class Ex09Bibliotheque(unittest.TestCase):
    def setUp(self): self.m=solution(9,'bibliotheque_json')
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'livres.json'
            b=self.m.Bibliotheque()
            b.ajouter(self.m.Livre('1','Les données','Ana'))
            b.sauvegarder(p)
            chargee=self.m.Bibliotheque.charger(p)
            self.assertEqual(chargee.rechercher('1').titre,'Les données')
    def test_doublon(self):
        b=self.m.Bibliotheque()
        b.ajouter(self.m.Livre('1','A','B'))
        with self.assertRaises(ValueError): b.ajouter(self.m.Livre('1','X','Y'))
    def test_fichier_absent(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError): self.m.Bibliotheque.charger(Path(d)/'inexistant.json')
    def test_fichier_invalide(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json';p.write_text('{mauvais json',encoding='utf-8')
            with self.assertRaises(ValueError): self.m.Bibliotheque.charger(p)


class Ex10Tabulate(unittest.TestCase):
    def setUp(self): self.m=solution(10,'catalogue_tabulate')
    def test_valeur_totale(self):
        c=self.m.Catalogue()
        c.ajouter(self.m.FicheProduit('A','Papeterie','2.5',4))
        c.ajouter(self.m.FicheProduit('B','Bureau','10',2))
        self.assertEqual(c.valeur_totale(),30)
    def test_filtre_trie(self):
        c=self.m.Catalogue()
        c.ajouter(self.m.FicheProduit('Z','A',1,1))
        c.ajouter(self.m.FicheProduit('B','A',1,1))
        self.assertEqual([p.reference for p in c.par_categorie('A')],['B','Z'])
    @unittest.skipUnless(importlib.util.find_spec('tabulate'), 'installer tabulate')
    def test_package_tableau(self):
        c=self.m.Catalogue()
        c.ajouter(self.m.FicheProduit('P','A',1,1))
        rendu=c.tableau()
        self.assertIn('Réf.',rendu)
        self.assertIn('P',rendu)
    def test_doublon(self):
        c=self.m.Catalogue()
        p=self.m.FicheProduit('P','A',1,1)
        c.ajouter(p)
        with self.assertRaises(ValueError): c.ajouter(p)


class Ex11Commande(unittest.TestCase):
    def setUp(self): self.m=solution(11,'commande')
    def test_parcours(self):
        c=self.m.Commande('C1')
        c.ajouter(self.m.LigneCommande('P',3,'5.5'))
        c.confirmer()
        self.assertEqual(c.total,Decimal('16.5'))
        c.expedier()
        self.assertEqual(c.statut,self.m.Statut.EXPEDIEE)
    def test_transition_interdite(self):
        c=self.m.Commande('C1')
        with self.assertRaises(ValueError): c.confirmer()
        c.ajouter(self.m.LigneCommande('P',1,5))
        c.confirmer()
        with self.assertRaises(ValueError): c.ajouter(self.m.LigneCommande('Q',1,5))
    def test_annulation(self):
        c=self.m.Commande('C1')
        c.annuler()
        self.assertEqual(c.statut,self.m.Statut.ANNULEE)
        with self.assertRaises(ValueError): c.confirmer()
    def test_immutable(self):
        l=self.m.LigneCommande('P',1,1)
        with self.assertRaises(FrozenInstanceError): l.quantite=2


class Ex12Repository(unittest.TestCase):
    def setUp(self): self.m=solution(12,'repository_json')
    def test_durable(self):
        with tempfile.TemporaryDirectory() as d:
            chemin=Path(d)/'clients.json'
            repo=self.m.RepositoryClientsJSON(chemin)
            repo.ajouter(self.m.Client('C1','Amina','amina@example.org'))
            self.assertEqual(self.m.RepositoryClientsJSON(chemin).obtenir('C1').nom,'Amina')
    def test_doublon(self):
        with tempfile.TemporaryDirectory() as d:
            repo=self.m.RepositoryClientsJSON(Path(d)/'clients.json')
            client=self.m.Client('C1','Amina','amina@example.org')
            repo.ajouter(client)
            with self.assertRaises(ValueError): repo.ajouter(client)
    def test_suppression(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'clients.json';repo=self.m.RepositoryClientsJSON(path)
            self.assertFalse(repo.supprimer('aucun'))
            repo.ajouter(self.m.Client('C1','Amina','amina@example.org'))
            self.assertTrue(repo.supprimer('C1'))
            self.assertIsNone(self.m.RepositoryClientsJSON(path).obtenir('C1'))
    def test_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'clients.json';path.write_text('{',encoding='utf-8')
            with self.assertRaises(ValueError): self.m.RepositoryClientsJSON(path)


class Ex13Strategies(unittest.TestCase):
    def setUp(self): self.m=solution(13,'strategies')
    def test_strategies_combinees(self):
        calc=self.m.Tarificateur()
        res=calc.calculer(100,[self.m.Pourcentage('0.1'),self.m.MontantFixe('5')])
        self.assertEqual(res,Decimal('85.00'))
    def test_remise_plafonnee(self):
        self.assertEqual(self.m.Tarificateur().calculer(10,[self.m.MontantFixe(20)]),0)
    def test_seuil(self):
        t=self.m.Tarificateur()
        self.assertEqual(t.calculer(30,[self.m.Seuil(50,10)]),30)
        self.assertEqual(t.calculer(50,[self.m.Seuil(50,10)]),40)
    def test_taux_invalide(self):
        with self.assertRaises(ValueError): self.m.Pourcentage(2)


@unittest.skipUnless(importlib.util.find_spec('pydantic'), 'installer pydantic>=2')
class Ex14Pydantic(unittest.TestCase):
    def setUp(self):
        self.m=solution(14,'pydantic')
        from pydantic import ValidationError
        self.ValidationError=ValidationError
    def test_total(self):
        c=self.m.CommandeAPI.model_validate({'client_id':' C1 ','lignes':[{'reference':'P1','quantite':2,'prix_unitaire':'12.5'}]})
        self.assertEqual(c.total,Decimal('25.0'))
        self.assertEqual(c.client_id,'C1')
    def test_doublon_refuse(self):
        with self.assertRaises(self.ValidationError):
            self.m.CommandeAPI.model_validate({'client_id':'C1','lignes':[
                {'reference':'P','quantite':1,'prix_unitaire':5},
                {'reference':'P','quantite':2,'prix_unitaire':3}]})
    def test_liste_vide_refusee(self):
        with self.assertRaises(self.ValidationError):
            self.m.CommandeAPI.model_validate({'client_id':'C1','lignes':[]})
    def test_quantite_entier_strict(self):
        with self.assertRaises(self.ValidationError):
            self.m.LigneAPI(reference='P1',quantite='2',prix_unitaire=5)
    def test_client_blanc_refuse(self):
        with self.assertRaises(self.ValidationError):
            self.m.CommandeAPI.model_validate({'client_id':'  ','lignes':[{'reference':'P','quantite':1,'prix_unitaire':1}]})


class Ex15Ordonnanceur(unittest.TestCase):
    def setUp(self): self.m=solution(15,'ordonnanceur')
    def test_ordre_simple(self):
        p=self.m.Projet()
        for id,deps in (('A',set()),('B',{'A'}),('C',{'B'})):
            p.ajouter(self.m.Tache(id,id,deps))
        self.assertEqual(p.ordre_execution(),['A','B','C'])
        self.assertEqual(p.taches_disponibles(),['A'])
    def test_prochaine_tache(self):
        p=self.m.Projet()
        p.ajouter(self.m.Tache('A','A'))
        p.ajouter(self.m.Tache('B','B',{'A'}))
        p.terminer('A')
        self.assertEqual(p.taches_disponibles(),['B'])
        with self.assertRaises(ValueError): p.terminer('A')
    def test_cycle(self):
        p=self.m.Projet()
        p.ajouter(self.m.Tache('A','A',{'B'}))
        p.ajouter(self.m.Tache('B','B',{'A'}))
        with self.assertRaises(self.m.DependancesCycliques): p.ordre_execution()
    def test_dependance_inconnue(self):
        p=self.m.Projet()
        p.ajouter(self.m.Tache('A','A',{'Z'}))
        with self.assertRaises(ValueError): p.ordre_execution()
    def test_tache_bloquee(self):
        p=self.m.Projet()
        p.ajouter(self.m.Tache('A','A'))
        p.ajouter(self.m.Tache('B','B',{'A'}))
        with self.assertRaises(ValueError): p.terminer('B')
    def test_independance_sets(self):
        deps={'A'}
        t=self.m.Tache('B','B',deps)
        deps.add('C')
        self.assertEqual(t.dependances,{'A'})


if __name__ == '__main__':
    unittest.main()
