#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>

#define BUFFSIZE 128
#define TASKSIZE 128
#define BAD_ID -1

/* User access level */
enum mode {USER, ADMIN};
enum task_state {ACTIVE, DELETED};
enum status {NEW, IN_PROGRESS, DONE};

struct task {
	int id;
	char name[BUFFSIZE];
	char content[BUFFSIZE];
	enum status state;
	void * run;
	char date_created_for_future_use[BUFFSIZE];
};

struct task_entry {
	enum mode level;
	enum task_state state;
	struct task* p_task;
};

struct task_entry tasks[TASKSIZE];
unsigned int n_tasks = 0;

void error(char * err) {
	/* Print error and quit */
	printf("Critical error : %s\n", err);
	exit(-1);
}

char get_char() {
	char buff[BUFFSIZE];
	fgets(buff, BUFFSIZE, stdin);
	return buff[0];
}

int authenticate() {
	/* Authenticate admin in order to modify / delete / run tasks */
	printf("Please enter admin password :\n");
	char password[BUFFSIZE];
	
	fgets(password, BUFFSIZE, stdin);
	strtok(password, "\n"); // Remove new line
	
	char admin_password[BUFFSIZE];
	int file_admin;

	file_admin = open("/home/task_manager/.password", O_RDONLY);
	if (file_admin != -1) {
		read(file_admin, admin_password, BUFFSIZE);
		strtok(admin_password, "\n"); // Remove new line too
	} else {
		error("Problem opening admin password file.\n");
	}
	close(file_admin);
	
	if (strlen(admin_password) < 16) {
		error("Problem opening admin password file.\n");
	}
	
	if (strcmp(admin_password, password) == 0) {
		printf("Logging as ADMIN\n");
		return ADMIN;
	} else {
		printf("Logging as regular USER\n");
		return USER;
	}
}

void debug_custom_users() {
	/* TODO IN_PROGRESS */
	int file_users_exist = access("/home/task_manager/.users", F_OK);
	if (file_users_exist != -1) {
		/* Handle user entries */
		printf("File already created !\n");
	} else {
		system("touch .users");
		printf("Append users list to the file and run again the program\n");
	}
}

void init_tasks() {
	/* Create some tasks */
	struct task* task_0 = (struct task *)malloc(sizeof(struct task));
	task_0->id = n_tasks;
	strcpy(task_0->name, "TODO ADMIN\n");
	strcpy(task_0->content, "Add function to save and restore tasks from files\n");
	task_0->state = NEW;
	
	tasks[n_tasks].level = ADMIN;
	tasks[n_tasks].state = ACTIVE;
	tasks[n_tasks++].p_task = task_0;
	
	struct task* task_1 = (struct task *)malloc(sizeof(struct task));
	task_1->id = n_tasks;
	strcpy(task_1->name, "TODO ADMIN 2\n");
	strcpy(task_1->content, "Add function to also authenticate users and read them from a file.\n");
	task_1->state = IN_PROGRESS;
	task_1->run = debug_custom_users;
	
	tasks[n_tasks].level = ADMIN;
	tasks[n_tasks].state = ACTIVE;
	tasks[n_tasks++].p_task = task_1;
	
	struct task* task_2 = (struct task *)malloc(sizeof(struct task));
	task_2->id = n_tasks;
	strcpy(task_2->name, "Welcome User\n");
	strcpy(task_2->content, "Invite users to my application ! Try to modify this task !\n");
	task_2->state = DONE;
	
	tasks[n_tasks].level = USER;
	tasks[n_tasks].state = ACTIVE;
	tasks[n_tasks++].p_task = task_2;
}

void print_menu() {
	printf("----- Task Manager -----\n");
	printf("  Commands :            \n");
	printf("    - list   task (l)   \n");
	printf("    - create task (c)   \n");
	printf("    - modify task (m)   \n");
	printf("    - delete task (d)   \n");
	printf("    - quit        (q)   \n");
	printf("  Only for admin tasks :\n");
	printf("    - run task    (r)   \n");
	printf("\n");
	printf("Your choice : \n");
}

void create_task() {
	/* Create new task at user or admin level */
	char level;
	
	printf("Create task for [a]dmin or [u]ser : \n");
	level = get_char();
	
	if (level == 'a') {
		tasks[n_tasks].level = ADMIN;
	} else if (level == 'u') {
		tasks[n_tasks].level = USER;
	} else {
		printf("Bad choice !\n");
		return;
	}
	struct task* new_task = (struct task *)malloc(sizeof(struct task));
	new_task->id = n_tasks;
	
	printf("Enter name : \n");
	fgets(new_task->name, BUFFSIZE, stdin);
	
	printf("Enter content : \n");
	fgets(new_task->content, BUFFSIZE, stdin);

	new_task->state = NEW;
	
	tasks[n_tasks].state = ACTIVE;
	tasks[n_tasks].p_task = new_task;
	
	printf("Task %d created with NEW state, you can modify it afterwards\n", n_tasks);
	n_tasks += 1;
}

int ask_task_id_and_check_level(int usermode) {
	/* Ask and check task ID */
	/* Also check task level */
	
	char buff[BUFFSIZE];
	
	printf("Enter task ID : \n");
	fgets(buff, BUFFSIZE, stdin);
	int id = atoi(buff);
	
	/* Check ID in range */
	if (id < 0 || id >= n_tasks) {
		printf("Bad identifier\n");
		return BAD_ID;
	}
	
	/* Check if level is the same or USER level to allow ADMIN to alter USER task */
	if (tasks[id].level == usermode || tasks[id].level == USER) {
		return id;
	}
	
	printf("You don't have the ADMIN access level\n");
	return BAD_ID;
}

void delete_task(int id) {
	/* Remove task from id */
	
	free(tasks[id].p_task);
	tasks[id].state = DELETED;
}

void list_tasks() {
	/* List active tasks */
	int i;
	printf("-----   Task List  -----\n");
	for (i = 0; i < n_tasks; i++) {
		if (tasks[i].state != DELETED) {
			if (tasks[i].level == USER)
				printf("  USER Task ID [%d] \n", i);
			else
				printf("  ADMIN Task ID [%d] \n", i);
			if (tasks[i].p_task->state == NEW)
				printf("  State : New\n");
			else if (tasks[i].p_task->state == IN_PROGRESS)
				printf("  State : In progress\n");
			else 
				printf("  State : Done \n");
			// Name and Content should be finished by \n
			printf("  Name  : %s", tasks[i].p_task->name);
			printf("  Content : %s", tasks[i].p_task->content);
			printf("        --------        \n");
		}
	}
	printf("\n");
}

void modify_task(struct task* p_task) {
	/* Modify task */
	
	char temp;
	char temp_buff[BUFFSIZE];
	
	/* Impossible to modify task name */
	printf("[not alterable] Name : %s", p_task->name);
	
	/* Modification of content (APPEND mode or ERASE mode) */
	if (strlen(p_task->content) > 0 && strlen(p_task->content) <= BUFFSIZE) {
		printf("Content : %s", p_task->content);
		printf("Do you want to [e]rase it or to [a]ppend data ?\n");
		temp = get_char();
		while (temp != 'e' && temp != 'a') {
			printf("Bad choice !\n");
			temp = get_char();
		}
		if (temp == 'a') {
			printf("%s", p_task->content);
			fflush(stdout);
			fgets(temp_buff, BUFFSIZE, stdin);
			strncat(p_task->content, temp_buff, BUFFSIZE);
		} else {
			printf("Enter content : \n");
			fgets(p_task->content, BUFFSIZE, stdin);
		}
	} else {
		printf("Enter content : \n");
		fgets(p_task->content, BUFFSIZE, stdin);
	}

	/* Modification of state */
	printf("Enter state ([n]ew, [i]n progress or [d]one): \n");
	temp = get_char();
	while (temp != 'n' && temp != 'i' && temp != 'd') {
		printf("Bad choice !\n");
		temp = get_char();
	}
	
	if (temp == 'n') {
		strcpy(temp_buff, "NEW");
		p_task->state = NEW;
	} else if (temp == 'i') {
		strcpy(temp_buff, "IN PROGESS");
		p_task->state = IN_PROGRESS;
	} else {
		strcpy(temp_buff, "DONE");
		p_task->state = DONE;
	}
	
	printf("Task %d modified with %s state.\n", p_task->id, temp_buff);
}

void run_task(struct task* p_task) {
	/* Run task ONLY FOR ADMIN TASK */
	
	void (*p_fct) ();
	p_fct = p_task->run;
	
	/* Check if task is an ADMIN TASK */
	if (tasks[p_task->id].level == ADMIN) {
		if (p_fct == 0) {
			printf("No function associated with the task !\n");
			return;
		}
		/* Run it */
		printf("Running task ...\n");
		p_fct();
		
	} else {
		printf("You can't run NON ADMIN task !\n");
	}
}

int main(int argc, char *argv[]) {
	setreuid(geteuid(), geteuid()); // avoid problem reading password file
	
	int usermode = authenticate();
	char choice;
	int id;
	
	init_tasks();

	while (1) {
		print_menu();
		choice = get_char();
		switch(choice) {
			
			/* Create Task */
			case 'c' :
				if (n_tasks >= TASKSIZE) {
					error("Too many tasks !\n");
				}
				create_task();
				break;
				
			/* Delete Task */
			case 'd' :
				id = ask_task_id_and_check_level(usermode);
				if (id == BAD_ID) {
					break;
				} else {
					delete_task(id);
				}
				break;
				
			/* List Tasks */
			case 'l' :
				list_tasks();
				break;
				
			/* Modify Task */
			case 'm' :
				id = ask_task_id_and_check_level(usermode);
				if (id == BAD_ID) {
					break;
				} else {
					modify_task(tasks[id].p_task);
				}
				break;
				
			/* Run Task */
			case 'r' :
				id = ask_task_id_and_check_level(usermode);
				if (id == BAD_ID) {
					break;
				} else {
					run_task(tasks[id].p_task);
				}
				break;
				
			/* Quit */
			case 'q' :
				exit(0);
				break;
				
			default :
				printf("Invalid choice\n");
		}

	}
	
	return 0;
}