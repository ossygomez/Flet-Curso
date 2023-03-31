from flet import (
    alignment,
    border_radius,
    colors,
    icons,
    margin,
    padding,
    Column,
    Container,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    Row,
    Text,
    TextField,
    UserControl
)


class Sidebar(UserControl):

    def __init__(self, app_layout, store: DataStore, page):
        super().__init__()

        self.app_layout = app_layout
        self.page = page

        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text('Boards'),
                label='boards',
                icon=icons.BOOK_OUTLINED,
                selected_icon=icons.BOOK_OUTLINED,
            ),
            NavigationRailDestination(
                label_content=Text('Members'),
                label='Members',
                icon=icons.PERSON,
                selected_icon=icons.PERSON,
            )
        ]

        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type='all',
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE_GREY,
            extended=True,
            expand=True
        )
        
        self.bottom_nav_rail = NavigationRail(
            selected_index=None,
            label_type='all',
            on_change=self.bottom_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE_GREY,
            extended=True,
            expand=True
        )

        self.toggle_nav_rail_button = IconButton(icons.ARROW_BACK)

    def build(self):
        self.view = Container (
            content=Column([
                Row([
                    Text('Workspace')
                ]),
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
                self.top_nav_rail,
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
            ],
            tight=True),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            bgcolor=colors.BLUE_GREY,
        )

        return self.view

    def sync_board_destinations(self):
        """
        Syncs the board destinations with the boards in the store.
        """
        boards = self.store.get_boards()
        self.bottom_nav_rail.destinations = []

        for i in range(len(boards)):
            b = boards[i]
            self.bottom_nav_rail.destinations.append(
                NavigationRailDestination(
                    label_content=TextField(
                        value=b.name,
                        hint_text=b.name,
                        text_size=12,
                        read_only=True,
                        on_focus=self.board_name_focus,
                        on_blur=self.board_name_blur,
                        border='none',
                        height=50,
                        width=150,
                        text_align='start',
                        data=i
                    ),
                    label=boards[i].name,
                    icon=icons.CHEVRON_RIGHT_OUTLINED,
                    selected_icon=icons.CHEVRON_RIGHT_ROUNDED,
                ),
            )
        
        self.view.update()
    
    def toggle_nav_rail(self):
        """
        Toggles the visibility of the sidebar.
        """
        self.view.visible = not self.view.visible
        self.view.update()
        self.page.update()
    
    def board_name_focus(self, event):
        """
        Sets the board name to editable when the text field is focused.
        """
        event.control.read_only = False
        event.control.border = 'outline'
        event.control.update()
    
    def board_name_blur(self, event):
        """
        Sets the board name to read-only when the text field is blurred.
        """
        self.store.update_board(self.store.get_boards()[event.control.data], {'name': event.control.value})

        self.app_layout.hydrate_all_boards_view()
        
        event.control.read_only = True
        event.control.border = 'none'
        self.page.update()

    def top_nav_change(self, event):
        self.top_nav_rail.selected_index = event.control.selected_index
        self.update()
