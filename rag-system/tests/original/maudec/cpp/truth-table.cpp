


bool _and(bool a1, bool a2) {
	if ((a1 == true) && (a2 == true)) {
		return true;
	}
	if ((a1 == true) && (a2 == false)) {
		return false;
	}
	if ((a1 == false) && (a2 == true)) {
		return false;
	}
	if ((a1 == false) && (a2 == false)) {
		return false;
	}
}

bool andc(bool a1, bool a2) {
	if ((a1 == true) && (a2 == true)) {
		return true;
	}
	if ((a1 == false) && (a2 == false)) {
		return false;
	}
	if ((a1 == true) && (a2 == false)) {
		return false;
	}
	if ((a1 == false) && (a2 == true)) {
		return false;
	}
}

