import PySimpleGUI as sg
from getGraph import MovieGraph
from algs import GraphAlgorithms
import plotly.graph_objects as go
import time

getDict = MovieGraph('movies_with_similar1.csv')
similarDict = getDict.get_similar_movies()
movieDict = getDict.get_title_to_id()
idDict = getDict.get_id_to_title()

layout = [
    [sg.Text('Select starting movie:')],
    [sg.Combo(list(movieDict.keys()), key='start_movie')],
    [sg.Text('Select destination movie:')],
    [sg.Combo(list(movieDict.keys()), key='end_movie')],
    [sg.Text('Select algorithm:')],
    [sg.Radio('A*', 'algorithms', key='Astar', default=True), sg.Radio("Dijkstra's", 'algorithms', key='Dijkstra'), sg.Radio('Bellman Ford', 'algorithms', key='Bellman')],
    [sg.Button('Find Shortest Path')],
]
window = sg.Window('Movie Vision', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Find Shortest Path':
        starting_movie = values['start_movie']
        ending_movie = values['end_movie']
        
        selected_algorithm = ''
        if values['Astar']:
            selected_algorithm = 'A*'
        elif values['Dijkstra']:
            selected_algorithm = "Dijkstra's"
        elif values['Bellman']:
            selected_algorithm = 'Bellman Ford'

        # visualize and show time taken
        start_time = time.time()
        if selected_algorithm == 'A*':
            result = GraphAlgorithms.astar(similarDict, idDict, movieDict[starting_movie], movieDict[ending_movie])
        elif selected_algorithm == "Dijkstra's":
            result = GraphAlgorithms.dijkstras(similarDict, idDict, movieDict[starting_movie], movieDict[ending_movie])
        elif selected_algorithm == 'Bellman Ford':
            result = GraphAlgorithms.bellman_ford(similarDict, idDict, movieDict[starting_movie], movieDict[ending_movie])
        end_time = time.time()

        if result:
            G = go.Figure()

            G.add_trace(go.Scatter(x=[i for i in range(len(result))], y=[0] * len(result),
                                mode='markers+text', marker=dict(size=20, color='skyblue'),
                                text=result, textposition='top center',
                                textfont=dict(size=10),
                                hoverinfo='text'))

            for i in range(len(result) - 1):
                G.add_trace(go.Scatter(x=[i, i + 1], y=[0, 0],
                                    mode='lines', line=dict(color='black'), hoverinfo='none'))

            G.update_layout(title=f'Shortest Path from {starting_movie} to {ending_movie}',
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                            hovermode='closest')

            G.show()

            sg.popup(f'Time taken by {selected_algorithm}: {end_time - start_time} seconds')
        else:
            sg.popup('No path found.')


window.close()
