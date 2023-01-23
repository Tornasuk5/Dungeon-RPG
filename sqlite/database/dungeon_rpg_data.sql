
/* -----------------------------------------------------
-------------------- CREATE TABLES --------------------
----------------------------------------------------- */

CREATE TABLE gear(
	id_gear SMALLINT PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	class VARCHAR(25) NOT NULL,
	level SMALLINT NOT NULL,
	defense SMALLINT NOT NULL,
	dodge DECIMAL(5, 2) NOT NULL
);

CREATE TABLE weapons(
	id_weapon SMALLINT PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	class VARCHAR(25) NOT NULL,
	level SMALLINT NOT NULL,
	attack SMALLINT NOT NULL,
	critical_hit DECIMAL(5, 2) NOT NULL
);

CREATE TABLE potions(
	id_potion SMALLINT PRIMARY KEY,
	name VARCHAR(45) NOT NULL,
	level SMALLINT NOT NULL,
	stat_rest VARCHAR(20) NOT NULL,
	amount_rest SMALLINT NOT NULL
);

CREATE TABLE floors(
	level SMALLINT PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	DESCRIPTION TEXT NOT NULL
);

CREATE TABLE classes(
	name VARCHAR(25) PRIMARY KEY,
	hp_init INT NOT NULL,
	mp_init INT NOT NULL,
	stamina_init INT NOT NULL,
	strength_init SMALLINT NOT NULL,
	agility_init SMALLINT NOT NULL,
	intellect_init SMALLINT NOT NULL,
	attack_init SMALLINT NOT NULL,
	defense_init SMALLINT NOT NULL,
	critical_hit_init DECIMAL(5, 2) NOT NULL,
	dodge_init DECIMAL(5, 2) NOT NULL
);

CREATE TABLE monsters (
	monster_type VARCHAR(25) PRIMARY KEY,
	level SMALLINT NOT NULL,
	hp INT NOT NULL,
	mp INT NOT NULL,
	stamina INT NOT NULL,
	strength SMALLINT NOT NULL,
	agility SMALLINT NOT NULL,
	intellect SMALLINT NOT NULL,
	attack SMALLINT NOT NULL,
	defense SMALLINT NOT NULL,
	critical_hit DECIMAL(5, 2) NOT NULL,
	dodge DECIMAL(5, 2) NOT NULL
);

CREATE TABLE classes_abilities(
	id_ability SMALLINT PRIMARY KEY,
	name VARCHAR(25) NOT NULL,
	level SMALLINT NOT NULL,
	attack_power SMALLINT NOT NULL,
	resources_cost SMALLINT NOT NULL,
	ref_class VARCHAR(25) NOT NULL,
    FOREIGN KEY (ref_class) REFERENCES classes (name)
);

CREATE TABLE monsters_abilities(
	id_ability SMALLINT PRIMARY KEY,
	name VARCHAR(25) NOT NULL,
	attack_power SMALLINT NOT NULL,
	resources_cost SMALLINT NOT NULL,
	probability SMALLINT NOT NULL,
	ref_monster_type VARCHAR(25) NOT NULL,
    FOREIGN KEY (ref_monster_type) REFERENCES monsters (monster_type)
);

CREATE TABLE characters (
	name VARCHAR(25) PRIMARY KEY,
	ref_class VARCHAR(25) NOT NULL,
	level SMALLINT NOT NULL,
	hp INT NOT NULL,
	mp INT NOT NULL,
	stamina INT NOT NULL,
	strength SMALLINT NOT NULL,
	agility SMALLINT NOT NULL,
	intellect SMALLINT NOT NULL,
	attack SMALLINT NOT NULL,
	defense SMALLINT NOT NULL,
	critical_hit DECIMAL(5, 2) NOT NULL,
	dodge DECIMAL(5, 2) NOT NULL,
	luck SMALLINT NOT NULL,
	ref_floor_level SMALLINT NOT NULL,
    FOREIGN KEY (ref_class) REFERENCES classes (name),
    FOREIGN KEY (ref_floor_level) REFERENCES floors (level)
);

CREATE TABLE characters_gear(
	id_cg SMALLINT PRIMARY KEY,
	ref_character VARCHAR(25) NOT NULL,
	ref_gear SMALLINT NOT NULL,
	equipped BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (ref_character) REFERENCES characters (name) ON DELETE CASCADE,
    FOREIGN KEY (ref_gear) REFERENCES gear (id_gear)
);

CREATE TABLE characters_weapons(
	id_cw SMALLINT PRIMARY KEY,
	ref_character VARCHAR(25) NOT NULL,
	ref_weapon SMALLINT NOT NULL,
	equipped BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (ref_character) REFERENCES characters (name) ON DELETE CASCADE,
    FOREIGN KEY (ref_weapon) REFERENCES weapons (id_weapon)
);

CREATE TABLE characters_potions(
	id_cp SMALLINT PRIMARY KEY,
	ref_character VARCHAR(25) NOT NULL,
	ref_potion SMALLINT NOT NULL,
    FOREIGN KEY (ref_character) REFERENCES characters (name) ON DELETE CASCADE,
    FOREIGN KEY (ref_potion) REFERENCES potions (id_potion)
);


/* -----------------------------------------------------
--------------------- INSERT DATA  --------------------
----------------------------------------------------- */

/* CLASSES */
INSERT INTO classes VALUES ('Hunter', 38, 0, 17, 1, 2, 1, 2, 1, 10, 5);
INSERT INTO classes VALUES ('Mage', 25, 21, 0, 1, 1, 2, 1, 1, 2.5, 1.5);
INSERT INTO classes VALUES ('Rogue', 35, 0, 17, 1, 2, 1, 3, 1, 20, 10);
INSERT INTO classes VALUES ('Warrior', 43, 0, 23, 2, 1, 1, 2, 2, 3.75, 1.25);

/* CLASSES_ABILITIES */
/* Hunter */
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Wind Shot', 1, 4, 1, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Survival Counterattack', 2, 6, 3, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Barrage', 3, 9, 5, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Arcane Shot', 4, 12, 7, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Fire Rain', 5, 17, 13, 'Hunter');

INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Elemental Shot', 6, 27, 20, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Raptor Edge', 7, 40, 30, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Hurricane', 8, 54, 40, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Stellar Eagle', 9, 71, 53, 'Hunter');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Thousand Arrows', 10, 90, 67, 'Hunter');

/* Mage */
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Frozen Spire', 1, 4, 2, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Fireball', 2, 7, 4, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Arcane Explosion', 3, 12, 8, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Blizzard', 4, 20, 12, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Mana Implosion', 5, 30, 22, 'Mage');

INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Phantom Spear', 6, 42, 34, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Magic Burst', 7, 56, 49, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Inferno', 8, 72, 67, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Desintegration', 9, 90, 87, 'Mage');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Nifleheim', 10, 100, 111, 'Mage');

/* Rogue */
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Sneak Stab', 1, 4, 2, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Shadow Blade', 2, 6, 3, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Bury Edge', 3, 9, 6, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Reaven Blades', 4, 14, 8, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Assassination', 5, 23, 14, 'Rogue');

INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Crimson Slash', 6, 34, 23, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Twin Fangs', 7, 48, 33, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Dance Macabre', 8, 63, 45, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Ryuuseigun', 9, 87, 58, 'Rogue');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Hissatsu', 10, 113, 74, 'Rogue');

/* Warrior */
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Cross Attack', 1, 4, 3, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Sword Thrust', 2, 6, 4, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Hammerfall', 3, 9, 7, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Illusory Blade', 4, 14, 15, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Duel of Spades', 5, 23, 26, 'Warrior');

INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Thunder Strike', 6, 36, 39, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Bladestorm', 7, 53, 55, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Titan Assault', 8, 72, 74, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Devastate', 9, 95, 96, 'Warrior');
INSERT INTO classes_abilities(name, level, attack_power, resources_cost, ref_class) VALUES('Worldsbreaker', 10, 120, 120, 'Warrior');

/* MONSTERS */
/* Lvl 1 */
INSERT INTO monsters VALUES('Undead', 1, 10, 0, 5, 1, 0, 0, 2, 0, 0, 0);
INSERT INTO monsters VALUES('Goblin', 1, 12, 0, 8, 1, 1, 1, 2, 1, 1.2, 1);
/* Lvl 2 */
INSERT INTO monsters VALUES('Cave Spider', 2, 16, 0, 10, 1, 2, 1, 3, 1, 2.4, 3);
INSERT INTO monsters VALUES('Skeleton Warrior', 2, 20, 0, 12, 2, 1, 0, 4, 1, 1, 0.5);
/* Lvl 3 */
INSERT INTO monsters VALUES('Dungeon Lizard', 3, 27, 0, 16, 2, 2, 1, 5, 1, 2, 2);
INSERT INTO monsters VALUES('Imp', 3, 23, 20, 0, 1, 2, 2, 4, 1, 2.4, 2.4);
/* Lvl 4 */
INSERT INTO monsters VALUES('Hellhound', 4, 38, 0, 26, 3, 3, 2, 8, 2, 3, 2.1);
INSERT INTO monsters VALUES('Shadow', 4, 36, 22, 0, 2, 3, 4, 6, 1, 2.1, 9);
/* Lvl 5 */
INSERT INTO monsters VALUES('Minotaur', 5, 45, 0, 40, 4, 3, 3, 11, 2, 5.1, 1.5);
INSERT INTO monsters VALUES('Stone Guardian', 5, 55, 0, 28, 4, 1, 1, 10, 3, 1.5, 0);
/* Lvl 6 */
INSERT INTO monsters VALUES('Crystal Scorpion', 6, 59, 0, 38, 4, 5, 3, 12, 3, 2.5, 2.5);
INSERT INTO monsters VALUES('Wyvern', 6, 76, 0, 44, 6, 4, 3, 17, 5, 1.2, 1.2);
/* Lvl 7 */
INSERT INTO monsters VALUES('Silver Fang', 7, 69, 0, 48, 5, 7, 5, 16, 3, 9.1, 9.1);
INSERT INTO monsters VALUES('Arachne', 7, 78, 65, 0, 4, 7, 7, 13, 2, 5.25, 3.5);
/* Lvl 8 */
INSERT INTO monsters VALUES('Daemon', 8, 96, 84, 0, 6, 5, 7, 20, 4, 5, 5);
INSERT INTO monsters VALUES('Reaper', 8, 119, 65, 0, 8, 6, 7, 28, 3, 12, 3);
/* Lvl 9 */
INSERT INTO monsters VALUES('Elder Lich', 9, 141, 130, 0, 5, 3, 9, 21, 3, 3, 0.7);
INSERT INTO monsters VALUES('Obsidian Guardian', 9, 156, 0, 98, 8, 5, 4, 27, 7, 5, 1.5);
INSERT INTO monsters VALUES('Behemoth', 9, 174, 121, 0, 9, 7, 7, 34, 5, 5.2, 3.5);
/* Lvl 10 */
INSERT INTO monsters VALUES('Black Dragon', 10, 500, 1000, 0, 10, 5, 10, 55, 10, 5, 0.5);

/* MONSTERS_ABILITIES */
/* Lvl 1 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Grip', 3, 3, 60, 'Undead');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Rotten Breath', 4, 3, 40, 'Undead');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Madness Attack', 4, 3, 50, 'Goblin');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Crazy Bite', 5, 3, 50, 'Goblin');
/* Lvl 2 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Web Shot', 5, 4, 70, 'Cave Spider');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Venomous Bite', 6, 5, 30, 'Cave Spider');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Bone Strike', 6, 6, 60, 'Skeleton Warrior');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Sword Shaking', 7, 7, 40, 'Skeleton Warrior');
/* Lvl 3 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Sink Claws', 8, 6, 55, 'Dungeon Lizard');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Tail Strike', 12, 8, 45, 'Dungeon Lizard');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Fireball', 10, 7, 75, 'Imp');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Devil`s Flame', 14, 8, 25, 'Imp');
/* Lvl 4 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Burning Bite', 13, 10, 70, 'Hellhound');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Infernal Jump', 17, 12, 30, 'Hellhound');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Obscure Attack', 12, 5, 60, 'Shadow');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Soul Piercing', 15, 7, 40, 'Shadow');
/* Lvl 5 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Fury', 17, 15, 60, 'Minotaur');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Titan Hack', 23, 18, 40, 'Minotaur');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Stone Crash', 16, 12, 70, 'Stone Guardian');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Stonequake', 22, 15, 30, 'Stone Guardian');
/* Lvl 6 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Crystals Rain', 19, 14, 75, 'Crystal Scorpion');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Mortal Sting', 22, 16, 25, 'Crystal Scorpion');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Fire Breath', 23, 17, 60, 'Wyvern');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Tail Spikes', 27, 20, 40, 'Wyvern');
/* Lvl 7 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Furious Pounce', 23, 16, 80, 'Silver Fang');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Bloody Fangs', 30, 20, 20, 'Silver Fang');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Labyrinth of Threads', 28, 22, 75, 'Arachne');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Shadow Binding', 35, 27, 25, 'Arachne');
/* Lvl 8 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Dark Flame', 36, 31, 85, 'Daemon');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Inferno', 42, 35, 15, 'Daemon');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Reap Soul', 50, 22, 70, 'Reaper');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Deathly Scythe', 55, 30, 30, 'Reaper');
/* Lvl 9 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Negative Burst', 44, 21, 80, 'Elder Lich');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Black Hole', 53, 27, 20, 'Elder Lich');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Obsidian Gaze', 35, 43, 75, 'Obsidian Guardian');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Ancient Swordsmanship', 43, 47, 25, 'Obsidian Guardian');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Earth Spear', 65, 50, 85, 'Behemoth');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Fire Nova', 72, 55, 15, 'Behemoth');
/* Lvl 10 */
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Dragon Breath', 88, 130, 55, 'Black Dragon');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Thunderstorm', 97, 150, 35, 'Black Dragon');
INSERT INTO monsters_abilities(name, attack_power, resources_cost, probability, ref_monster_type) VALUES('Time Tearing', 111, 200, 10, 'Black Dragon');

/* GEAR */
/* Lvl 1 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(1, 'Leather Armor (Hunter)', 'Hunter', 1, 1, 0);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(2, 'Leather Armor (Rogue)', 'Rogue', 1, 1, 0);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(3, 'Cloth Armor', 'Mage', 1, 1, 0);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(4, 'Plate Armor', 'Warrior', 1, 1, 0);
/* Lvl 2 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(5, 'Forestman Armor', 'Hunter', 2, 2, 0.25);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(6, 'Opportunist Armor', 'Rogue', 2, 2, 0.5);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(7, 'Arcanist Armor', 'Mage', 2, 1, 0.2);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(8, 'Swordman Armor', 'Warrior', 2, 2, 0.15);
/* Lvl 3 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(9, 'Predator Armor', 'Hunter', 3, 2, 0.5);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(10, 'Thief Armor', 'Rogue', 3, 2, 1);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(11, 'Frostfire Armor', 'Mage', 3, 1, 0.4);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(12, 'Warbringer Armor', 'Warrior', 3, 3, 0.5);
/* Lvl 4 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(13, 'Windrunner Armor', 'Hunter', 4, 3, 0.75);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(14, 'Blackfang Armor', 'Rogue', 4, 3, 0.8);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(15, 'Silvermoon Armor', 'Mage', 4, 2, 0.75);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(16, 'Destroyer Armor', 'Warrior', 4, 4, 0.25);
/* Lvl 5 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(17, 'Bloodhunter Armor', 'Hunter', 5, 4, 0.75);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(18, 'Shadowblade Armor', 'Rogue', 5, 4, 1);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(19, 'Time Lord`s Armor', 'Mage', 5, 2, 1);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(20, 'Siegebreaker Armor', 'Warrior', 5, 5, 0.75);
/* Lvl 6 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(21, 'Howling Beast`s Armor', 'Hunter', 6, 5, 1);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(22, 'Deathbringer Armor', 'Rogue', 6, 5, 1.5);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(23, 'Archmage Armor', 'Mage', 6, 4, 0.75);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(24, 'Dragonplate Armor', 'Warrior', 6, 6, 0.5);
/* Lvl 7 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(25, 'Dragonstalker Armor', 'Hunter', 7, 6, 2);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(26, 'Nightslayer Armor', 'Rogue', 7, 6, 2.5);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(27, 'Firelord Armor', 'Mage', 7, 5, 1);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(28, 'Vengeful Gladiator`s Armor', 'Warrior', 7, 7, 1);
/* Lvl 8 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(29, 'Dark Phoenix Armor', 'Hunter', 8, 7, 3);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(30, 'Armor of the Silent Assassin', 'Rogue', 8, 7, 4);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(31, 'Armor of the Frozen Scroll', 'Mage', 8, 6, 1.5);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(32, 'Armor of Conquest', 'Warrior', 8, 8, 2);
/* Lvl 9 */
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(33, 'Armor of the Unblinking Vigil', 'Hunter', 9, 8, 3.5);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(34, 'Armor of the Thousandfold Blades', 'Rogue', 9, 8, 5);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(35, 'Armor of the Elemental Triad', 'Mage', 9, 7, 2);
INSERT INTO gear(id_gear, name, class, level, defense, dodge) VALUES(36, 'Armor of the Iron Wrath', 'Warrior', 9, 10, 2.5);

/* WEAPONS */
/* Lvl 1 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(1, 'Wooden Bow', 'Hunter', 1, 1, 0.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(2, 'Metal Daggers', 'Rogue', 1, 2, 0.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(3, 'Wooden Staff', 'Mage', 1, 1, 0);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(4, 'Metal Sword', 'Warrior', 1, 2, 0);
/* Lvl 2 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(5, 'Elven Bow', 'Hunter', 2, 2, 1);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(6, 'Blood-Guided Knifes', 'Rogue', 2, 2, 1.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(7, 'Balanced Spell Staff', 'Mage', 2, 1, 0.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(8, 'Mithril Sword', 'Warrior', 2, 2, 0.5);
/* Lvl 3 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(9, 'Shadowleaf Bow', 'Hunter', 3, 3, 1);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(10, 'Ebony Daggers', 'Rogue', 3, 3, 2);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(11, 'Earthborn Staff', 'Mage', 3, 2, 0.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(12, 'Swiftwind Sword', 'Warrior', 3, 3, 0.75);
/* Lvl 4 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(13, 'Huntmaster`s Longbow', 'Hunter', 4, 4, 1.75);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(14, 'Dawn Blades', 'Rogue', 4, 4, 2.25);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(15, 'Iceberg Staff', 'Mage', 4, 3, 1);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(16, 'Fighter Broadsword', 'Warrior', 4, 4, 1.25);
/* Lvl 5 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(17, 'Razorwind Bow', 'Hunter', 5, 5, 2);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(18, 'Runesong Daggers', 'Rogue', 5, 5, 2.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(19, 'Thunder Owl Staff', 'Mage', 5, 4, 1.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(20, 'Howling Sword', 'Warrior', 5, 5, 1.5);
/* Lvl 6 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(21, 'Hawkeye Bow', 'Hunter', 6, 6, 3);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(22, 'Darkblood Daggers', 'Rogue', 6, 6, 4);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(23, 'Runetotem Staff', 'Mage', 6, 5, 2);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(24, 'Sword of the Empty Void', 'Warrior', 6, 6, 2.5);
/* Lvl 7 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(25, 'Storm`s Bow', 'Hunter', 7, 7, 2.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(26, 'Phantom Daggers', 'Rogue', 7, 7, 5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(27, 'Frostbitten Staff', 'Mage', 7, 6, 2);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(28, 'Tempest of Chaos', 'Warrior', 7, 7, 3);
/* Lvl 8 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(29, 'Twilight Longbow', 'Hunter', 8, 8, 4);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(30, 'Daggers of Wretched Spectres', 'Rogue', 8, 8, 7.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(31, 'Staff of the Mist Navigator', 'Mage', 8, 7, 3);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(32, 'Sword of the Falling Sky', 'Warrior', 8, 8, 3);
/* Lvl 9 */
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(33, 'Longbow of the Ruby Rider', 'Hunter', 9, 9, 5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(34, 'Blades of the Uncrowned', 'Rogue', 9, 10, 10);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(35, 'Staff of The Old One', 'Mage', 9, 8, 3.5);
INSERT INTO weapons(id_weapon, name, class, level, attack, critical_hit) VALUES(36, 'The Black Knight', 'Warrior', 9, 10, 4);

/* POTIONS */
/* Lvl 1 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(1, 'Lesser Healing Potion', 1, 'HP', 10);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(2, 'Lesser Mana Potion', 1, 'MP', 10);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(3, 'Lesser Stamina Potion', 1, 'Stamina', 10);
/* Lvl 2 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(4, 'Minor Healing Potion', 2, 'HP', 25);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(5, 'Minor Mana Potion', 2, 'MP', 15);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(6, 'Minor Stamina Potion', 2, 'Stamina', 15);
/* Lvl 3 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(7, 'Healing Potion', 3, 'HP', 30);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(8, 'Mana Potion', 3, 'MP', 20);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(9, 'Stamina Potion', 3, 'Stamina', 20);
/* Lvl 4 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(10, 'Powerlful Healing Potion', 4, 'HP', 40);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(11, 'Powerlful Mana Potion', 4, 'MP', 25);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(12, 'Powerlful Stamina Potion', 4, 'Stamina', 25);
/* Lvl 5 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(13, 'Major Healing Potion', 5, 'HP', 50);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(14, 'Major Mana Potion', 5, 'MP', 30);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(15, 'Major Stamina Potion', 5, 'Stamina', 30);
/* Lvl 6 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(16, 'Runic Healing Potion', 6, 'HP', 65);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(17, 'Runic Mana Potion', 6, 'MP', 35);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(18, 'Runic Stamina Potion', 6, 'Stamina', 35);
/* Lvl 7 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(19, 'Superior Healing Potion', 7, 'HP', 80);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(20, 'Superior Mana Potion', 7, 'MP', 40);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(21, 'Superior Stamina Potion', 7, 'Stamina', 40);
/* Lvl 8 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(22, 'Greater Healing Potion', 8, 'HP', 100);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(23, 'Greater Mana Potion', 8, 'MP', 50);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(24, 'Greater Stamina Potion', 8, 'Stamina', 50);
/* Lvl 9 */
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(25, 'Mighty Healing Potion', 9, 'HP', 150);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(26, 'Mighty Mana Potion', 9, 'MP', 70);
INSERT INTO potions(id_potion, name, level, stat_rest, amount_rest) VALUES(27, 'Mighty Stamina Potion', 9, 'Stamina', 70);


/* FLOORS */
/* Lvl 1 */
INSERT INTO floors VALUES(1, 'The Passage', 'The main entrance to the deepest dungeon in the land. It is a treacherous corridor in which some low level monsters like undeads and goblins usually spawn...');
/* Lvl 2 */
INSERT INTO floors VALUES(2, 'Mausoleum', 'You stand now in front of a big gate made of stone, the entrance to the second floor. It seems the gate`s frame represents some kind of battle. Behind it, you glimpse some old tombs among a dense fog, and something moving through it...');
/* Lvl 3 */
INSERT INTO floors VALUES(3, 'Pillars Hall', 'You arrive to an inmense hall full of black stone pillars. This pillars produce some kind of faint lights that light up a path through the entire floor, somehow...');
/* Lvl 4 */
INSERT INTO floors VALUES(4, 'Shadow Nest', 'Once you have crossed the hall, you stare at a big hole in the floor from which you can only see darkness. But the more you stare into this hole, the more you realize there are something shifting inside it...');
/* Lvl 5 */
INSERT INTO floors VALUES(5, 'The Labyrinth', 'You manage to get out of that dark place and now you arrive to the entrace of what looks like an intrincate labyrinth. You start to hear heavy footsteps and the sounds of what seems an axe being dragged...');
/* Lvl 6 */
INSERT INTO floors VALUES(6, 'Crystal Caverns', 'At the end of the labyrinth, you see some stairs surrounded by purple crystals going deep down to the sixth floor. Some magic essence is pouring out of them, maybe this could have attracted some monsters...
');
/* Lvl 7 */
INSERT INTO floors VALUES(7, 'The Dark Descent', 'Is this a sort of inverted tower? You wonder. The almost endless spiral staircase surrounded by red torchlights in front of you goes down and down, reaching what seems the bottom of the dungeon...
');
/* Lvl 8 */
INSERT INTO floors VALUES(8, 'Red Corridors', 'Once you arrive at the bottom, you gaze the entrance of a perturbing corridor. Its walls seem to exude a red liquid very similar to blood, and you can glance the unsettling shifting of shadows on the ceiling...');
/* Lvl 9 */
INSERT INTO floors VALUES(9, 'The Unnamed`s Tomb', 'You stand in front of the Doom`s Gates. Behind it lies the prison of a legendary demon who almost corrupted and destroyed the world five centuries ago. Due to its immeasurable power, this place is guarded by the obsidian guardians, but they are not the only creatures down here...');
/* Lvl 10 */
INSERT INTO floors VALUES(10, 'The Broken Throne', 'The very end of the dungeon. Anyone has ever reached this point, but you have managed to end here. In front of you lies The Unnamed`s Tomb`s throne room, a great chamber full of treasures that has been occupied by a mighty black dragon...');