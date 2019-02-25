class gen_algo:
    def __init__(self):
        nb_run = 1    # nb de run par bot
        nb_move = 200 # nb de move par run
        nb_start_pop = 400 # nb de bot dans la pop de depart
        list_bot = []

    def gen_start_pop(self):
        # generation de la pop de depart
        for i in range(0, nb_start_pop):
            list_bot.append(Bot())

    def start(self):
        # boucle de generation
        for i in range(1, 4000000):
            print(" ")
            print("======================================================")
            print("Generation: ", i, " | game run, nb bots:", len(list_bot))

            list_fitness_overall = []
            list_lignes_overall = []

            # on fait jouer chaque bot
            for bot in tqdm(list_bot):
                # creation
                model = gen_NN(bot.genes)
                bot.genes = model.get_weights()
                for piece_set in pieces_set:
                    game_run(bot, model, nb_move=nb_move, piece_set=copy.deepcopy(piece_set))
                list_fitness_overall.append(bot.get_fitness())
                list_lignes_overall.append(bot.get_lines_cleared())
                keras.backend.clear_session()

            # trie des bots par ordre de fitness
            list_bot.sort(key=lambda x: (x.get_lines_cleared(), x.get_fitness()), reverse=True)
            new_list_bot = []

            list_fitness = []
            print("moyenne des fitness: ", np.mean(list_fitness_overall))
            print("moyenne des lignes: ", np.mean(list_lignes_overall))
            # selection des x meilleurs bots
            for j in range(0, 10):
                new_list_bot.append(list_bot[j])
                list_fitness.append((list_bot[j].get_lines_cleared(), list_bot[j].get_fitness()))

            print("resultat des boss: ", list_fitness)
            #plt.plot([ [bot.get_lines_cleared(), bot.get_fitness() ] for bot in list_bot])
            #plt.show()
            if i > 1:
                model = gen_NN(new_list_bot[0].genes)
                game_run(new_list_bot[0], model, draw_enable=draw_enable, nb_move=100, piece_set=copy.copy(pieces_set[0]))
                print("resultat du meilleur: ",new_list_bot[0].get_lines_cleared(), " lignes cleared")
                print(new_list_bot[0].genes[0][0])

            list_bot = []

            l = len(new_list_bot)

            list_enfants = []

            # croisement
            for k in range(1, l):

                b1 = new_list_bot[l- k]
                b2 = new_list_bot[l- k - 1]

                list_bot.append(b1)
                #list_bot.append(b2)

                list_croisement = croisement(b1.genes, b2.genes, 10)

                for enfant in mutate_list(list_croisement, 6, 2):
                    list_bot.append(Bot(enfant))
