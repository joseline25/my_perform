$(document).ready(() => {
	let step1 = true;
	// $(".action-phrase-input").val("");
	// $(".number-input").val("");
	// $(".units-input").val("");
	// $("[type='number']").keypress(function (evt) {
	// 	evt.preventDefault();
	// });
	let objectiveType = "Financial";
	let objectivePriority = "Low";
	//trigger click for the objective type radio button with value Financial
	$(".objective-type input[type='radio'][value='Financial']").trigger(
		"click"
	);
	//make sure only a class of objective-type with with input type radio is selected
	$(".objective-type input[type='radio']").click((e) => {
		e.stopPropagation();
		objectiveType = $(e.target).val();
		console.log($(e.target).val());
	});

	$(".objective-priority").click((e) => {
		e.stopPropagation();
		objectivePriority = $(e.target).val();
	});

	//set objective priority select input to Low
	$(".objective-priority").val("Low");
	//set objective complexity to Easy
	$(".objective-complexity").val("Easy");

	$(".step1-dot").addClass("active");
	$("#step2").addClass("d-none");
	$(".prev").addClass("d-none");
	$(".start-date").val(new Date().toISOString().slice(0, 10));
	$(".repeat-date").val(new Date().toISOString().slice(0, 10));
	$(".end-date-input").val(new Date().toISOString().slice(0, 10));
	$(".deadline-input").val(new Date().toISOString().slice(0, 10));

	$(".prev").click((e) => {
		e.preventDefault();
		e.stopPropagation();
		$("#step1").removeClass("d-none");
		$("#step2").addClass("d-none");
		$(".prev").addClass("d-none");
		$(".next").removeClass("d-none");
		$(".step1-dot").removeClass("finish");
		$(".step1-dot").addClass("active");
		$(".step2-dot").removeClass("active");
		step1 = true;
	});
	$(".next").click((e) => {
		e.preventDefault();
		e.stopPropagation();

		let action_phrase = $(".action-phrase-input").val();
		let number = $(".number-input").val();
		let units = $(".units-input").val();
		let deadline = $(".deadline-input").val();

		if (!action_phrase || !number || !units || !deadline) {
			applyErrorLabel(action_phrase, number, units, deadline);
			$(".modal-error").trigger("click");
			return;
		} else {
			$(".lbl-action-phrase").removeClass("text-danger fw-bold");
			$(".lbl-number").removeClass("text-danger fw-bold");
			$(".lbl-units").removeClass("text-danger fw-bold");
			$(".lbl-deadline").removeClass("text-danger fw-bold");
		}
		//check if any of the option checkboxes are checked
		if ($(".option input[type='checkbox']:checked").length == 0) {
			$(".lbl-dog").addClass("text-danger fw-bold").prop("hidden", false);
			return;
		} else {
			$(".lbl-dog")
				.removeClass("text-danger fw-bold")
				.prop("hidden", true);
		}
		//check which objective type radio button is selected
		if (
			(objectiveType === "Financial" && objectivePriority === "Low") ||
			(objectivePriority === "High" && objectiveType === "Non-Financial")
		) {
			$(".plain-warning-text").html(
				"You are trying to set the priority of a <span class='fw-bold'>Financial Objective</span> to <span class='fw-bold'>LOW</span>."
			);
			$(".objective-warning-priority-modal").trigger("click");
		} else {
			$("#step1").addClass("d-none");
			$("#step2").removeClass("d-none");
			$(".next").addClass("d-none");
			$(".prev").removeClass("d-none");
			$(".step1-dot").removeClass("active");
			$(".step1-dot").addClass("finish");
			$(".step2-dot").addClass("active");
			step1 = false;
		}
		if (objectiveType === "Non-Financial" && objectivePriority === "High") {
			$(".plain-warning-text").html(
				"You are trying to set the priority of a <span class='fw-bold'>Non-Financial Objective</span> to <span class='fw-bold'>High</span>."
			);
			$(".objective-warning-priority-modal").trigger("click");
		}
	});

	$(".priority-accept").click((e) => {
		e.stopPropagation();
		$("#step1").addClass("d-none");
		$("#step2").removeClass("d-none");
		$(".next").addClass("d-none");
		$(".prev").removeClass("d-none");
		$(".step1-dot").removeClass("active");
		$(".step1-dot").addClass("finish");
		$(".step2-dot").addClass("active");
		step1 = false;
	});

	$(".repeatradio").click((e) => {
		e.stopPropagation();
		console.log("radio1", $(".repeatradio").attr("checked"));
	});

	//functions
	//apply error label to empty input fields
	const applyErrorLabel = (action_phrase, number, units, deadline) => {
		if (!action_phrase)
			$(".lbl-action-phrase").addClass("text-danger fw-bold");
		if (!number) $(".lbl-number").addClass("text-danger fw-bold");
		if (!units) $(".lbl-units").addClass("text-danger fw-bold");
		if (!deadline) $(".lbl-deadline").addClass("text-danger fw-bold");
	};

	//dropdown
	$(".option input[type='checkbox']").each(function () {
		$(this).attr("check", "unchecked");
	});

	// Open dropdown when clicking on the button
	$(".dropdown-selected").on("click", function (e) {
		e.stopPropagation();
		$(".dropdown-container").toggleClass("open");
	});
	// Open tool dropdown when clicking on the button
	$(".tools-dropdown-selected").on("click", function (e) {
		e.stopPropagation();
		$(".tools-dropdown-container").toggleClass("open").slideDown();
	});
	// Open visibleTo dropdown when clicking on the button
	$(".visibleTo-dropdown-selected").on("click", function (e) {
		e.stopPropagation();
		$(".visibleTo-dropdown-container").toggleClass("open").slideDown();
	});
	// Open visibleTo dropdown when clicking on the button
	$(".assignTo-dropdown-selected").on("click", function (e) {
		e.stopPropagation();
		$(".assignTo-dropdown-container").toggleClass("open").slideDown();
	});
	// Open evaluator dropdown when clicking on the button
	$(".evaluator-dropdown-selected").on("click", function (e) {
		e.stopPropagation();
		$(".evaluator-dropdown-container").toggleClass("open").slideDown();
	});
	// Open skills dropdown when clicking on the button
	$(".skills-dropdown-selected").on("click", function (e) {
		e.stopPropagation();
		$(".skills-dropdown-container").toggleClass("open").slideDown();
	});
	// Open skills dropdown when clicking on the button
	$(".suggestedTask-dropdown-selected").on("click", function (e) {
		e.stopPropagation();
		$(".suggestedTask-dropdown-container").toggleClass("open").slideDown();
	});
	// Close dropdown when clicking outside
	$(document).on("click", function () {
		$(".dropdown-container").removeClass("open");
		$(".tools-dropdown-container").removeClass("open");
		$(".visibleTo-dropdown-container").removeClass("open");
		$(".assignTo-dropdown-container").removeClass("open");
		$(".evaluator-dropdown-container").removeClass("open");
		$(".skills-dropdown-container").removeClass("open");
		$(".suggestedTask-dropdown-container").removeClass("open");
	});

	// Prevent dropdown from closing when clicking inside the dropdown
	$(".dropdown-options").on("click", function (e) {
		e.stopPropagation();
	});
	// Prevent dropdown from closing when clicking inside the dropdown
	$(".tools-dropdown-options").on("click", function (e) {
		e.stopPropagation();
	});
	// Prevent dropdown from closing when clicking inside the dropdown
	$(".visibleTo-dropdown-options").on("click", function (e) {
		e.stopPropagation();
	});
	// Prevent dropdown from closing when clicking inside the dropdown
	$(".assignTo-dropdown-options").on("click", function (e) {
		e.stopPropagation();
	});
	// Prevent dropdown from closing when clicking inside the dropdown
	$(".evaluator-dropdown-options").on("click", function (e) {
		e.stopPropagation();
	});
	// Prevent dropdown from closing when clicking inside the dropdown
	$(".skills-dropdown-options").on("click", function (e) {
		e.stopPropagation();
	});
	// Prevent dropdown from closing when clicking inside the dropdown
	$(".suggestedTask-dropdown-options").on("click", function (e) {
		e.stopPropagation();
	});
	//make sure no option checkboxes is checked
	$(".option input[type='checkbox']").prop("checked", false);

	//make sure no tools option checkboxes is checked
	$(".tools-dropdown-options > .option input[type='checkbox']").prop(
		"checked",
		false
	);
	//make sure no visibleTo option checkboxes is checked
	$(".visibleTo-dropdown-options > .option input[type='checkbox']").prop(
		"checked",
		false
	);
	//make sure no assignTo option checkboxes is checked
	$(".assignTo-dropdown-options > .option input[type='checkbox']").prop(
		"checked",
		false
	);
	//make sure no evaluator option checkboxes is checked
	$(".evaluator-dropdown-options > .option input[type='checkbox']").prop(
		"checked",
		false
	);
	//make sure no skills option checkboxes is checked
	$(".skills-dropdown-options > .option input[type='checkbox']").prop(
		"checked",
		false
	);
	//make sure no associated Task option checkboxes is checked
	$(".suggestedTask-dropdown-options > .option input[type='checkbox']").prop(
		"checked",
		false
	);

	//bind a click event to all option divs
	$(".dropdown-options .option").on("click", function () {
		const checkbox = $(this).find("input[type='checkbox']");
		checkbox.prop("checked", !checkbox.prop("checked"));
		updateSelectedOptions();
	});
	//bind a click event to all tools option divs
	$(".tools-dropdown-options >.option").on("click", function () {
		const checkbox = $(this).find("input[type='checkbox']");
		checkbox.prop("checked", !checkbox.prop("checked"));
		updateSelectedToolsOptions();
	});
	//bind a click event to all visibleTo option divs
	$(".visibleTo-dropdown-options >.option").on("click", function () {
		const checkbox = $(this).find("input[type='checkbox']");
		checkbox.prop("checked", !checkbox.prop("checked"));
		updateSelectedVisibleToOptions();
	});
	$(".assignTo-dropdown-options >.option").on("click", function () {
		const checkbox = $(this).find("input[type='checkbox']");
		checkbox.prop("checked", !checkbox.prop("checked"));
		updateSelectedAssignToOptions();
	});
	$(".evaluator-dropdown-options >.option").on("click", function () {
		const checkbox = $(this).find("input[type='checkbox']");
		checkbox.prop("checked", !checkbox.prop("checked"));
		updateSelectedEvaluatorOptions();
	});
	$(".skills-dropdown-options >.option").on("click", function () {
		const checkbox = $(this).find("input[type='checkbox']");
		checkbox.prop("checked", !checkbox.prop("checked"));
		updateSelectedSkillsOptions();
	});
	$(".suggestedTask-dropdown-options >.option").on("click", function () {
		const checkbox = $(this).find("input[type='checkbox']");
		checkbox.prop("checked", !checkbox.prop("checked"));
		updateSelectedSuggestedTasksOptions();
	});
	//bind a click event to all option checkboxes
	$(".option input[type='checkbox']").on("click", function (e) {
		e.stopPropagation(); // Prevent the click from propagating to the parent .option
		updateSelectedOptions();
	});
	$(".tools-dropdown-options .option input[type='checkbox']").on(
		"click",
		function (e) {
			e.stopPropagation(); // Prevent the click from propagating to the parent .option
			updateSelectedToolsOptions();
		}
	);
	$(".visibleTo-dropdown-options .option input[type='checkbox']").on(
		"click",
		function (e) {
			e.stopPropagation(); // Prevent the click from propagating to the parent .option
			updateSelectedVisibleToOptions();
		}
	);
	$(".assignTo-dropdown-options .option input[type='checkbox']").on(
		"click",
		function (e) {
			e.stopPropagation(); // Prevent the click from propagating to the parent .option
			updateSelectedAssignToOptions();
		}
	);
	$(".evaluator-dropdown-options .option input[type='checkbox']").on(
		"click",
		function (e) {
			e.stopPropagation(); // Prevent the click from propagating to the parent .option
			updateSelectedEvaluatorOptions();
		}
	);
	$(".skills-dropdown-options .option input[type='checkbox']").on(
		"click",
		function (e) {
			e.stopPropagation(); // Prevent the click from propagating to the parent .option
			updateSelectedSkillsOptions();
		}
	);
	$(".suggestedTask-dropdown-options .option input[type='checkbox']").on(
		"click",
		function (e) {
			e.stopPropagation(); // Prevent the click from propagating to the parent .option
			updateSelectedSuggestedTasksOptions();
		}
	);

	//watch for input in the custom dog input
	$(".custom-dog-input").keyup(function (e) {
		$(this).val() && $(".add-dog-btn").prop("disabled", false);
		!$(this).val() && $(".add-dog-btn").prop("disabled", true);
	});

	//add a new dog
	$(".add-dog-btn").click((e) => {
		e.stopPropagation();

		const child = `<div class="option">
				<input
					type="checkbox"
					class="checkbox"
					value="${$(".custom-dog-input").val()}"
				/>
				${$(".custom-dog-input").val()}
			</div>`;

		$(".dropdown-options").append(child);

		//bind a click event to the new checkbox
		$(".option input[type='checkbox']").on("click", function (e) {
			e.stopPropagation();
			updateSelectedOptions();
		});
		//bind a click even to the new option
		$(".option:last").on("click", function () {
			const checkbox = $(this).find("input[type='checkbox']");
			checkbox.prop("checked", !checkbox.prop("checked"));
			updateSelectedOptions();
		});

		//make only the new checkbox checked
		$(".option input[type='checkbox']:last").prop("checked", true);

		//update the selected options
		updateSelectedOptions();

		$(".custom-dog-input").val("");
		!$(".custom-dog-input").val() &&
			$(".add-dog-btn").prop("disabled", true);
	});

	//cancle adding a new dog
	$(".cancle-dog-btn").click((e) => {
		e.stopPropagation();
		$(".custom-dog-input").val("");
		!$(".custom-dog-input").val() &&
			$(".add-dog-btn").prop("disabled", true);
	});

	$(".add-btn").click(() => {
		//change font size of the input placeholder
		$(".custom-dog-input").css("font-size", "12px").css("padding", "10px");
	});

	// $(".option input[type='checkbox']").on("change", function () {});
	function updateSelectedOptions() {
		const selectedOptions = $(".option input[type='checkbox']:checked")
			.map(function () {
				return `<div class = "dog-chip">${$(this).val()}</div>`;
			})
			.get();
		$(".dropdown-selected").html(
			selectedOptions.length > 0
				? selectedOptions.join(" ")
				: "Select Criteria(s)"
		);
	}
	function updateSelectedToolsOptions() {
		const selectedOptions = $(
			".tools-dropdown-options .option input[type='checkbox']:checked"
		)
			.map(function () {
				return `<div class = "dog-chip">${$(this).val()}</div>`;
			})
			.get();
		$(".tools-dropdown-selected").html(
			selectedOptions.length > 0
				? selectedOptions.join(" ")
				: "Select Tool(s)"
		);
	}
	function updateSelectedVisibleToOptions() {
		const selectedOptions = $(
			".visibleTo-dropdown-options .option input[type='checkbox']:checked"
		)
			.map(function () {
				return `<div class = "dog-chip">${$(this).val()}</div>`;
			})
			.get();
		$(".visibleTo-dropdown-selected").html(
			selectedOptions.length > 0
				? selectedOptions.join(" ")
				: "<span class = 'text-secondary'><i class='bi bi-person-circle' style='margin-right: 8px; font-size: 20px'></i></span><span style='margin-top: 5px;'>Select one or more</span>"
		);
	}
	function updateSelectedAssignToOptions() {
		const selectedOptions = $(
			".assignTo-dropdown-options .option input[type='checkbox']:checked"
		)
			.map(function () {
				return `<div class = "dog-chip">${$(this).val()}</div>`;
			})
			.get();
		$(".assignTo-dropdown-selected").html(
			selectedOptions.length > 0
				? selectedOptions.join(" ")
				: "<span class = 'text-secondary'><i class='bi bi-person-circle' style='margin-right: 8px; font-size: 20px'></i></span><span style='margin-top: 5px;'>Select one or more</span>"
		);
	}
	function updateSelectedEvaluatorOptions() {
		const selectedOptions = $(
			".evaluator-dropdown-options .option input[type='checkbox']:checked"
		)
			.map(function () {
				return `<div class = "dog-chip">${$(this).val()}</div>`;
			})
			.get();
		$(".evaluator-dropdown-selected").html(
			selectedOptions.length > 0
				? selectedOptions.join(" ")
				: "<span class = 'text-secondary'><i class='bi bi-person-circle' style='margin-right: 8px; font-size: 20px'></i></span><span style='margin-top: 5px;'>Select one or more</span>"
		);
	}
	function updateSelectedSkillsOptions() {
		const selectedOptions = $(
			".skills-dropdown-options .option input[type='checkbox']:checked"
		)
			.map(function () {
				return `<div class = "dog-chip">${$(this).val()}</div>`;
			})
			.get();
		$(".skills-dropdown-selected").html(
			selectedOptions.length > 0
				? selectedOptions.join(" ")
				: "Select one or more"
		);
	}

	function updateSelectedSuggestedTasksOptions() {
		const selectedOptions = $(
			".suggestedTask-dropdown-options .option input[type='checkbox']:checked"
		)
			.map(function () {
				return `<div class = "dog-chip">${$(this).val()}</div>`;
			})
			.get();
		$(".suggestedTask-dropdown-selected").html(
			selectedOptions.length > 0
				? selectedOptions.join(" ")
				: "Select one or more suggested tasks"
		);
	}
});
