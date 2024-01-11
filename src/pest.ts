import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';

// /*
//  * $editpestModal: required
//  * options: optional
//  */

// // For your js code

interface IPest {
  id: number;
  name: string;
  symptoms: string;
  treatment: string;
}

const $modalElement: HTMLElement = document.querySelector('#editPestModal');
const $addpestModalElement: HTMLElement =
  document.querySelector('#add-pest-modal');

const modalOptions: ModalOptions = {
  placement: 'bottom-right',
  backdrop: 'dynamic',
  backdropClasses:
    'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
  closable: true,
  onHide: () => {
    console.log('modal is hidden');
  },
  onShow: () => {
    console.log('pest id: ');
  },
  onToggle: () => {
    console.log('modal has been toggled');
  },
};

const modal: ModalInterface = new Modal($modalElement, modalOptions);
const addModal: ModalInterface = new Modal($addpestModalElement, modalOptions);

const $buttonElements = document.querySelectorAll('.pest-edit-button');
$buttonElements.forEach(e =>
  e.addEventListener('click', () => {
    editPest(JSON.parse(e.getAttribute('data-target')));
  }),
);

// closing add edit modal
const $buttonClose = document.querySelector('#modalCloseButton');
if ($buttonClose) {
  $buttonClose.addEventListener('click', () => {
    modal.hide();
  });
}

// closing add pest modal
const addModalCloseBtn = document.querySelector('#modalAddCloseButton');
if (addModalCloseBtn) {
  addModalCloseBtn.addEventListener('click', () => {
    addModal.hide();
  });
}

// search flow
const searchInput: HTMLInputElement = document.querySelector(
  '#table-search-pests',
);
const searchInputButton = document.querySelector('#table-search-pest-button');
if (searchInputButton && searchInput) {
  searchInputButton.addEventListener('click', () => {
    const url = new URL(window.location.href);
    url.searchParams.set('q', searchInput.value);
    window.location.href = `${url.href}`;
  });
}
const deleteButtons = document.querySelectorAll('.delete-pest-btn');

deleteButtons.forEach(e => {
  e.addEventListener('click', async () => {
    if (confirm('Are sure?')) {
      let id = e.getAttribute('data-pest-id');
      const response = await fetch(`/pest/delete/${id}`, {
        method: 'DELETE',
      });
      if (response.status == 200) {
        location.reload();
      }
    }
  });
});

function editPest(pest: IPest) {
  let input: HTMLInputElement = document.querySelector('#pest-edit-name');
  input.value = pest.name;
  input = document.querySelector('#pest-edit-id');
  input.value = pest.id.toString();
  input = document.querySelector('#pest-edit-symptoms');
  input.value = pest.symptoms;
  input = document.querySelector('#pest-edit-treatment');
  input.value = pest.treatment;
  input = document.querySelector('#pest-edit-next_url');
  input.value = window.location.href;
  modal.show();
}
