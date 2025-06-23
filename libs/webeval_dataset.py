#TODO: This file is NOT comlpete yet. TODO: Complete it and make it useable.
import rp
rp.pip_import('dict_hash')

import dict_hash
import rp.web_evaluator as wev

class TicketHandler(rp.CachedInstances):
    #Input tickets are json-like easydicts
    #Output tickets are easydict dict[str->Any Type, but particularly paths to files]
    #This class might be instantiated many times, so if something needs GPU and need to load a model,
    #best to do that globally as a singleton.
    #KEEP THIS CLASS LEAN! It will be pickled and passed by value at each call. This class should NOT hold much data.
    #No more than a kilobyte preferably.

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def get_output_ticket(self, input_ticket):
        #THIS BLOCK SHOULD BE ABSTRACTED
        #AND DOCSTRING IT...IT SHOULD BE SIMPLE TO UNDERSTAND IF NOT WE NEED TO RETHINK IT
        output_ticket = rp.as_easydict()
        processed_ticket = self.process_ticket(input_ticket)
        sample_folder = self.get_sample_folder(input_ticket)

        for name, value in processed_ticket:
            if name in self.CACHE_PATHS:

                file_name = self.CACHE_PATHS[name]
                file_path = rp.path_join(sample_folder, file_name)

                if not self.path_exists(file_path):
                    #If value is passed as a callable, only evaluate it 
                    #if we need to fill the cache
                    if callable(value):
                        value = value()

                    #Compute the value and cache it
                    value = value()
                    self.save_file(value, file_path)
                    output_ticket[value] = file_path

        return output_ticket

    def save_ticket(self, output_ticket, folder=None):
        #output_ticket is dict of filenames -> values
        #For things without an extension, we pass them by value - so we don't save them
        #Returns an output ticket (easydict of str -> value)
    
        output_ticket = rp.as_easydict()

        for name, value in output_ticket.items():
            #Like key=="video.mp4" --> We save the value
            #Key like "video" --> we return the value directly
            
            if name in self.CACHE_PATHS:
                file_path = rp.path_join(folder, self.CACHE_PATHS[name])
                value = self.save_file(value, file_path)
                assert isinstance(value, str), f'self.save_file should return a path, but got type {type(value)}'
            
            output_ticket[name] = value
        
        return output_ticket
    
    def get_ticket_hashname(input_ticket):
        #Maybe you want some semantic info in the name...idk. So this is overrideable
        #But should be unique per input ticket!
        return dict_hash.sha256(input_ticket)[:10]
    
    def get_sample_folder(self, input_ticket):
        return rp.path_join(self.cache_dir, self.get_ticket_hashname(input_ticket))

    def load_sample(self, output_ticket):
        return rp.as_easydict(
            {
                key: self.load_file(value) if isinstance(value, str) and rp.get_file_name(value) in self.CACHE_PATHS else value
                for key, value in output_ticket.items()
            }
        )
    
    def __repr__(self):
        ...
        #TODO
    


    ##### THE BELOW FUNCTIONS ARE COMPUTE-PLATFORM-SPECIFIC #####
    ##### IF CHANGED, IT SHOULD BE VIA A PLATFORM MIXIN OR SOMETHING... #####
    ##### IF YOU HAVE NFS, OR ARE WORKING ON A SINGLE MACHINE - NO CHANGES ARE NEEDED #####

    def save_file(self, object, path):
        #Save a file, return the file path as str
        return rp.r._omni_save(object, path)
    
    def load_file(self, path):
        #On XCloud it would be nice to have used 
        #If you're using cloud storage like AWS, this is the place to put the download functionality!
        #If you ever have to download anything (and not just read the path), make sure you delete it before exiting this function
        return rp.r._omni_load(path)
    
    def path_exists(self, path):
        #NOTE: If you're going to use URL's or such you should implement another thing to check if said URL's exist here, this only checks paths right now...
        return rp.path_exists(path)

    def paths_exist(self, paths):
        #Might be room for optimization on some platforms...
        return all(self.path_exists(path) for path in paths)


    ##### THE BELOW CODE SHOULD BE CHANGED ON A PER-DATASET BASIS #####
    ##### BE IT A VIDEO DATASET, IMAGE DATASET, SNORLAX DATASET #####
    ##### ALL PREPROCESSING IS SPECIFIED IN THE BELOW FUNCTION, GPU OR NOT #####

    #ALL KEYS SHOULD BE NAMESPACEABLE
    #PATHS CAN BE NESTED IF NEEDED, LIKE 'low_quality/video.mp4'
    CACHE_PATHS = dict(
        video_480p49 = 'video.mp4',
        input_ticket = 'input_ticket.json',
    )

    def process_ticket(self, input_ticket):
        #TODO: THIS FUNCTION NEEDS A BETTER NAME
        #TODO: Docstring this func, explain how the output should be dict of namespaceable names to either callables or values
        #And that if in CACHE_PATHS, it will save it in cache as a file 
        #And that also, if in CACHE_PATHS if given as a callable, will be called and evaluated IF AND ONLY IF we need to fill the cache
        #This is the sauce you need to change for better dataloaders
        #This is a potential example
        #This func does not handle caching! That's handled elsewhere
        #You'll want to subclass this func if you need GPU functionality and preprocessing etc
        #We're providing just the basics here
        #Yugly lol this docstring is messy mess ur job to clean it

        def get_video():
            raw_video = rp.load_video(input_ticket.raw_video_path)
            video = rp.resize_list(rp.resize_images(raw_video, size=(480,720)),49)
            with rp.temporary_seed_all(input_ticket.seed):
                if rp.random_chance():
                    #Augmentation via random seed example
                    video = video.flip(2)
            return video
            
        return dict(
            video_480p49 = get_video,
            input_ticket = input_ticket,
            **input_ticket, #Includes prompt, raw_video_path - passed by value because not in CACHE_PATHS
        )
    
class LocalDataset:
    def __init__(self, input_tickets, ticket_handler: TicketHandler):
        self.input_tickets = self.load_input_tickets(input_tickets)
        self.ticket_handler = ticket_handler

    def load_input_tickets(self, input_tickets):
        #Ticket roll can be passed as value or by path
        #Path could be a .csv or a .tsv or an list of [str->[int, float, str]] dicts pickled value
        #If you want to preprocess the list of tickets, playing with seeds etc -
        #  or mix multiple together, this is the place to do it!

        if isinstance(input_tickets, str):
            input_tickets = self.load_file(input_tickets)

        if hasattr(input_tickets, 'to_dict'):
            #Given a pandas table, turn it into a list of dicts
            input_tickets=rp.list_dict_transpose(input_tickets.to_dict())

        #Output should be a list of easydicts, all with string keys
        return input_tickets

    def get_output_ticket(self, input_ticket):
        return self.ticket_handler.get_output_ticket(input_ticket)
    
    def __getitem__(self, index):
        input_ticket = self.input_tickets[index]
        output_ticket = self.get_output_ticket(input_ticket)

        return self.load_sample(output_ticket)

    def __len__(self):
        return len(self.input_tickets)
    
    def __repr__(self):
        return f'{type(self).__name__}(len={len(self)}, ticket_handler={self.ticket_handler})'
    
class RemoteDataset(LocalDataset):
    def __init__(self, input_tickets, ticket_handler:TicketHandler, delegator: wev.DelegationClient):
        super().__init__(input_tickets=input_tickets, ticket_handler=ticket_handler)
        self.delegator=delegator
    
    def get_output_ticket(self, input_ticket):
        output = self.delegator.evaluate(
            "ticket_handler.get_output_ticket(input_ticket)",
            ticket_handler=self.ticket_handler,
            input_ticket=input_ticket,
        )
        if output.errored:
            raise output.error
        return output.value
        
    def __repr__(self):
        return f'{type(self).__name__}(len={len(self)}, ticket_handler={self.ticket_handler}, delegator={self.delegator})'

    @classmethod
    def launch_cluster(
        cls,
        input_tickets,
        ticket_handler,
        num_workers=8,
        *,
        session_name=None,
        base_port=None,
        python_executable=None,
        command_before=None,
        attach=False,
        roster=None,
        delegator_port=None,
        ip_address=None,
        # Different from defaults
        if_exists="replace",
    ):
        if session_name is None:
            session_name = cls.__name__

        cluster_info = wev.launch_tmux_delegation_cluster(
            num_delegatees=num_workers,
            base_port=base_port,
            python_executable=python_executable,
            command_before=command_before,
            attach=attach,
            roster=roster,
            delegator_port=delegator_port,
            ip_address=ip_address,
            if_exists=if_exists,
        )

        delegator = cluster_info.delegator

        return cls(
            input_tickets=input_tickets,
            ticket_handler=ticket_handler,
            delegator=delegator,
        )

