from __future__ import annotations

from typing import Dict, List, Sequence


class StyledWizardMixin:
    """Shared presentation logic for multi-step registration wizards."""

    template_name: str = "register/wizard_form.html"
    wizard_title: str = ""
    step_titles: Dict[str, str] = {}
    field_layout: Dict[str, Sequence[Sequence[str]]] = {}
    next_button_label: str = "Próximo"
    done_button_label: str = "Concluir cadastro"

    def get_template_names(self) -> List[str]:
        return [self.template_name]

    # --- Step metadata helpers -------------------------------------------------
    def get_step_titles(self) -> Dict[str, str]:
        return self.step_titles

    def _normalize_label(self, step_key: str) -> str:
        labels = self.get_step_titles()
        label = labels.get(step_key)
        if label:
            return label
        # Fallback: humanize the key
        return step_key.replace("_", " ").title()

    def _get_step_keys(self) -> List[str]:
        form_list = self.get_form_list()
        return list(form_list.keys())

    def _build_steps_metadata(self) -> List[Dict[str, object]]:
        keys = self._get_step_keys()
        return [
            {
                "key": key,
                "index": idx + 1,
                "label": self._normalize_label(key),
            }
            for idx, key in enumerate(keys)
        ]

    # --- Field layout helpers --------------------------------------------------
    def get_field_layout(self) -> Dict[str, Sequence[Sequence[str]]]:
        return self.field_layout

    def _build_field_rows(self, form, step_key: str) -> List[List[str]]:
        layout_config = self.get_field_layout().get(step_key, [])
        field_order = list(form.fields.keys())
        # Use the first field of each configured group as lookup key.
        group_lookup = {group[0]: group for group in layout_config if group}
        rows: List[List[str]] = []
        used: set[str] = set()

        for name in field_order:
            if name in used:
                continue

            group = group_lookup.get(name)
            if group and all(member in form.fields for member in group):
                rows.append(list(group))
                used.update(group)
            else:
                rows.append([name])
                used.add(name)

        return rows

    # --- Context ----------------------------------------------------------------
    def get_extra_context(self, form, current_step: str) -> Dict[str, object]:
        return {}

    def get_context_data(self, form, **kwargs):  # type: ignore[override]
        context = super().get_context_data(form=form, **kwargs)

        step_keys = self._get_step_keys()
        if not step_keys:
            return context

        current_step = self.steps.current
        try:
            step_index = step_keys.index(current_step)
        except ValueError:
            step_index = 0

        steps_metadata = self._build_steps_metadata()
        is_last_step = current_step == step_keys[-1]

        context.update(
            {
                "wizard_title": self.wizard_title,
                "steps_metadata": steps_metadata,
                "current_step_index": step_index + 1,
                "is_last_step": is_last_step,
                "submit_label": self.done_button_label if is_last_step else self.next_button_label,
                "field_rows": self._build_field_rows(form, current_step),
            }
        )
        context.update(self.get_extra_context(form, current_step))
        return context


class RegistrationSuccessMixin:
    """Shared context for the success page displayed after the wizard."""

    template_name: str = "register/success.html"
    wizard_title: str = ""
    steps_metadata: Sequence[Dict[str, object]] = ()
    success_title: str = "Cadastro concluído com sucesso!"
    success_messages: Sequence[str] = ()
    cta_url: str | None = None
    cta_label: str = ""
    success_icon: str | None = "imgs/icons/discount-icon.svg"

    def get_template_names(self) -> List[str]:
        return [self.template_name]

    def get_steps_metadata(self) -> List[Dict[str, object]]:
        return [dict(step) for step in self.steps_metadata]

    def get_current_step_index(self) -> int:
        steps = self.get_steps_metadata()
        return len(steps)

    def get_success_messages(self) -> List[str]:
        return list(self.success_messages)

    def get_cta_url(self) -> str | None:
        return self.cta_url

    def get_cta_label(self) -> str:
        return self.cta_label

    def get_success_icon(self) -> str | None:
        return self.success_icon

    def get_extra_context(self) -> Dict[str, object]:
        return {}

    def get_context_data(self, **kwargs):  # type: ignore[override]
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "wizard_title": self.wizard_title,
                "steps_metadata": self.get_steps_metadata(),
                "current_step_index": self.get_current_step_index(),
                "success_title": self.success_title,
                "success_messages": self.get_success_messages(),
                "cta_url": self.get_cta_url(),
                "cta_label": self.get_cta_label(),
                "success_icon": self.get_success_icon(),
            }
        )
        context.update(self.get_extra_context())
        return context
