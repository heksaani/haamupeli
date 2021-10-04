import pygame, random

class HaamuPeli:
    def __init__(self):
        pygame.init()
 
        self.korkeus = 480
        self.leveys = 640
 
        self.lataa_kuvat()
 
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
 
        self.fontti = pygame.font.SysFont("Arial", 24)
 
        pygame.display.set_caption("Haamu peli")
 
        self.silmukka()
 
    def lataa_kuvat(self):
        self.robo = pygame.image.load("robo.png")
        self.kolikko = pygame.image.load("kolikko.png")
        self.haamu = pygame.image.load("hirvio.png")
 
    def silmukka(self):
        self.uusi_peli()
        self.vasemmalle = False
        self.oikealle = False
        self.ylos = False
        self.alas = False
 
        self.kello = pygame.time.Clock()
 
        while True:
            self.tutki_tapahtumat()
            self.liiku()
            self.piirra_naytto()
 
 
    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True

                if tapahtuma.key == pygame.K_TAB:
                    self.silmukka()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
 
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
            if tapahtuma.type == pygame.QUIT:
                exit() 
 
 
    def liiku(self):
        if self.vasemmalle and self.robo_x > 0:
            self.robo_x -= 2
 
        if self.oikealle and self.robo_x < self.leveys - self.robo.get_width():
            self.robo_x += 2

        if self.ylos and self.robo_y > 0:
            self.robo_y -= 2 

        if self.alas and self.robo_y < self.korkeus - self.robo.get_height():
            self.robo_y += 2 

        self.haamu_x += self.haamun_nopeus_x
        self.haamu_y += self.haamun_nopeus_y

        if self.haamu_x == 0 or self.haamu_x+ self.haamu.get_width() == self.leveys:
            self.haamun_nopeus_x = -self.haamun_nopeus_x
        if self.haamu_y == 0 or self.haamu_y+self.haamu.get_height() == self.korkeus:
            self.haamun_nopeus_y = -self.haamun_nopeus_y        

 
    def uusi_peli(self):
        self.pisteet = 0
        self.elamat = 3
 
        self.robo_x = self.leveys/2-self.robo.get_width()/2
        self.robo_y = self.korkeus/2-self.robo.get_height()/2
 
        self.kolikot = []
        for i in range(15):
            kolikko_x = random.randint(0, self.leveys - self.kolikko.get_width())
            kolikko_y = random.randint(-2500, 0 - self.kolikko.get_height())
            self.kolikot.append([kolikko_x, kolikko_y])

        
        self.haamu_x = 0
        self.haamu_y = 0
        self.haamun_nopeus_x = 2
        self.haamun_nopeus_y = 2



 
    def piirra_naytto(self):
        if not self.havisit() and not self.voitit():
            self.naytto.fill((255, 255, 255))

            for i in range(15):
                self.naytto.blit(self.kolikko, (self.kolikot[i][0], self.kolikot[i][1]))
                self.kolikot[i][1] += 1.5
 
                if self.kolikot[i][0] >= self.robo_x - self.kolikko.get_width() and self.kolikot[i][0] <= self.robo_x + self.robo.get_width():
                    if self.kolikot[i][1] >= self.robo_y - self.kolikko.get_height() and self.kolikot[i][1] <= self.robo_y + self.robo.get_height():
                        self.kolikot[i][0] = random.randint(0, self.leveys - self.kolikko.get_width())
                        self.kolikot[i][1] = random.randint(-2500, 0 - self.kolikko.get_height())
                        self.pisteet += 1

                if self.kolikot[i][1] + self.kolikko.get_height() > self.korkeus:
                    self.kolikot[i][0] = random.randint(0, self.leveys - self.kolikko.get_width())
                    self.kolikot[i][1] = random.randint(-2500, 0 - self.kolikko.get_height())                    
 

            self.naytto.blit(self.haamu, (self.haamu_x, self.haamu_y))
            self.naytto.blit(self.robo, (self.robo_x, self.robo_y))
            

            if self.haamu_x >= self.robo_x - self.haamu.get_width() and self.haamu_x <= self.robo_x + self.robo.get_width():
                if self.haamu_y >= self.robo_y - self.haamu.get_height() and self.haamu_y <= self.robo_y + self.robo.get_height():
                    self.elamat -= 1
                    self.haamu_y = 0
                    self.haamu_x = 0

            teksti = self.fontti.render(f"Kolikot: {self.pisteet}   Elämät: {self.elamat}", True, (200, 0, 0))
            self.naytto.blit(teksti, (420, 5))
 
            
            
            pygame.display.flip()
 
            self.kello.tick(60)
 
        if self.havisit():
 
            teksti1 = self.fontti.render(f"HÄVISIT!", True, (200, 0, 0))
            teksti2 = self.fontti.render(f"TAB = uusi peli", True, (200, 0, 0))
            teksti3 = self.fontti.render(f"Esc = sulje peli", True, (200, 0, 0))
            self.naytto.blit(teksti1, (self.leveys/2 - teksti1.get_width()/2, 150))
            self.naytto.blit(teksti2, (self.leveys/2 - teksti2.get_width()/2, 220))
            self.naytto.blit(teksti3, (self.leveys/2 - teksti3.get_width()/2, 250))
 
            pygame.display.flip()
 
        if self.voitit():
            teksti1 = self.fontti.render(f"Voitit pelin!", True, (200, 0, 0))
            teksti2 = self.fontti.render(f"TAB = uusi peli", True, (200, 0, 0))
            teksti3 = self.fontti.render(f"Esc = sulje peli", True, (200, 0, 0))
            self.naytto.blit(teksti1, (self.leveys/2 - teksti1.get_width()/2, 150))
            self.naytto.blit(teksti2, (self.leveys/2 - teksti2.get_width()/2, 220))
            self.naytto.blit(teksti3, (self.leveys/2 - teksti3.get_width()/2, 250))
            
            pygame.display.flip()


    def havisit(self):
        if self.elamat <= 0:
            return True
        return False

    def voitit(self):
        if self.pisteet == 10:
            return True
        return False
 
 
if __name__ == "__main__":
    HaamuPeli()